from typing import List
import uuid

import pandas as pd
from sqlalchemy.engine.base import Connection


def write_to_sql(
    con: Connection, table: str, df: pd.DataFrame, table_type: str
) -> None:
    """
    SQL Table function to store a Pandas DataFrame to a SQL Table

    Args:
        con (Connection): The connection to the SQL DB.

        table (str): The Table name to write to SQL as.

        df (DataFrame): The Pandas DataFrame to store in SQL

        table_type (str): Whether the table should replace or append to an existing SQL Table under that name

    Returns:
        Writes the Pandas DataFrame to a Table in the Schema we connected to.

    """
    try:
        if len(df) == 0:
            print(f"{table} is empty, not writing to SQL")
        else:
            df.to_sql(
                con=con,
                name=f"{table}",
                index=False,
                if_exists=table_type,
            )
            print(f"Writing {len(df)} {table} rows to {table} to SQL")
    except BaseException as error:
        print(f"SQL Write Script Failed, {error}")


def write_to_sql_upsert(
    conn,
    table: str,
    schema: str,
    df: pd.DataFrame,
    table_type: str,
    pd_index: List[str],
) -> None:
    """
    SQL Table function to upsert a Pandas DataFrame into a SQL Table.

    Will create a new table if it doesn't exist.  If it does, it will insert new records and upsert new column values onto existing records (if applicable).

    You have to do some extra index stuff to the pandas df to specify what the primary key of the records is (this data does not get upserted).

    Args:
        conn (SQL Connection): The connection to the SQL DB.

        table (str): The Table name to write to SQL as.

        schema (str): The Name of the SQL Schema the table is in

        df (DataFrame): The Pandas DataFrame to store in SQL

        table_type (str): A placeholder which should always be "upsert"

        pd_index (List[str]): The columns that make up the composite primary key of the SQL Table.

    Returns:
        Upserts any new data in the Pandas DataFrame to the table in Postgres in the provided schema

    """
    sql_table_name = f"{table}"
    if len(df) == 0:
        print(f"{sql_table_name} is empty, not writing to SQL")
        pass

    else:
        # 2 try except blocks bc in event of an error there needs to be different logic to safely exit out and continue script
        try:
            df = df.set_index(pd_index)
            df = df.rename_axis(pd_index)

            if not conn.execute(
                f"""SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE  table_schema = '{schema}' 
                    AND table_name = '{sql_table_name}');
                    """
            ).first()[0]:
                # If the table does not exist, we should just use to_sql to create it
                df.to_sql(sql_table_name, conn)
                print(
                    f"SQL Upsert Function Successful, {len(df)} records added to a NEW TABLE {sql_table_name}"
                )
                pass
        except BaseException as error:
            print(
                f"SQL Upsert Function Failed for NEW TABLE {sql_table_name} ({len(df)} rows), {error}"
            )
            pass
        else:
            try:
                # If it already exists...
                temp_table_name = f"temp_{uuid.uuid4().hex[:6]}"
                df.to_sql(temp_table_name, conn, index=True)

                index = list(df.index.names)
                index_sql_txt = ", ".join([f'"{i}"' for i in index])
                columns = list(df.columns)
                headers = index + columns
                headers_sql_txt = ", ".join([f'"{i}"' for i in headers])
                # this is excluding the primary key columns needed to identify the unique rows.
                update_column_stmt = ", ".join(
                    [f'"{col}" = EXCLUDED."{col}"' for col in columns]
                )

                # For the ON CONFLICT clause, postgres requires that the columns have unique constraint
                query_pk = f"""
                ALTER TABLE "{sql_table_name}" DROP CONSTRAINT IF EXISTS unique_constraint_for_upsert_{table};
                ALTER TABLE "{sql_table_name}" ADD CONSTRAINT unique_constraint_for_upsert_{table} UNIQUE ({index_sql_txt});
                """

                conn.execute(query_pk)

                # Compose and execute upsert query
                query_upsert = f"""
                INSERT INTO "{sql_table_name}" ({headers_sql_txt}) 
                SELECT {headers_sql_txt} FROM "{temp_table_name}"
                ON CONFLICT ({index_sql_txt}) DO UPDATE 
                SET {update_column_stmt};
                """
                conn.execute(query_upsert)
                conn.execute(f"DROP TABLE {temp_table_name};")
                print(
                    f"SQL Upsert Function Successful, {len(df)} records added or upserted into {table}"
                )
                pass
            except BaseException as error:
                conn.execute(f"DROP TABLE {temp_table_name};")
                print(
                    f"SQL Upsert Function Failed for EXISTING {table} ({len(df)} rows), {error}"
                )
                pass

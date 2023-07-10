from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def sql_connection(
    database: str,
    schema: str,
    user: str,
    pw: str,
    host: str,
) -> Engine:
    """
    SQL Engine function to define the SQL Driver + connection variables needed to connect to the DB.
    This doesn't actually make the connection, use conn.connect() in a context manager to create 1 re-usable connection

    Args:
        database(str): The Database to connect to

        schema (str): The Schema to connect to

        user (str): The User for the connection

        pw (str): The Password for the connection

        host (str): The Host Endpoint of the Database

    Returns:
        SQL Engine variable to a specified schema in my PostgreSQL DB
    """
    connection = create_engine(
        f"postgresql+psycopg2://{user}:{pw}@{host}:5432/{database}",
        # pool_size=0,
        # max_overflow=20,
        connect_args={
            "options": f"-csearch_path={schema}",
        },
        # defining schema to connect to
        echo=False,
    )
    print(f"SQL Engine for schema: {schema} Successful")
    return connection

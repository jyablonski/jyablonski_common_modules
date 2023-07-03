from sqlalchemy import exc, create_engine
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
        rds_schema (str): The Schema in the DB to connect to.

    Returns:
        SQL Engine variable to a specified schema in my PostgreSQL DB
    """
    try:
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
    except exc.SQLAlchemyError as e:
        print(f"SQL Engine for schema: {schema} Failed, Error: {e}")
        return e

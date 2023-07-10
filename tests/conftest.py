from datetime import datetime
import os
import time

import pandas as pd
import pytest

from jyablonski_common_modules.general import get_feature_flags
from jyablonski_common_modules.sql import sql_connection


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["USER_EMAIL"] = "jyablonski9@gmail.com"
    os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = 1
    # ^ some dumbass mf shit lmfao


@pytest.fixture(scope="session")
def postgres_conn():
    """Fixture to connect to Docker Postgres Container"""
    conn = sql_connection(
        database="postgres",
        schema="sales_source",
        user="postgres",
        pw="postgres",
        host="localhost",
    )

    connection = conn.connect()
    yield connection


@pytest.fixture(scope="session")
def sales_data():
    """Fixture for Write to SQL Upsert Test"""
    data = {
        "id": [2, 4],
        "item": ["Sandals", "Belt"],
        "price": [10, 100],
    }
    df = pd.DataFrame(data=data)
    return df


@pytest.fixture(scope="session")
def shipping_data():
    """Fixture for Write to SQL Test"""
    date = datetime.now().date()

    data = {
        "id": [1, 2, 3],
        "shipping_location": ["Seattle", "San Antonio", "Chicago"],
        "shipping_destination": ["Los Angeles", "New York City", "Miami"],
        "date": [date, date, date],
    }
    df = pd.DataFrame(data=data)
    return df


@pytest.fixture(scope="session")
def get_feature_flags_postgres(postgres_conn):
    time.sleep(3)
    feature_flags = get_feature_flags(connection=postgres_conn, schema="sales_source")

    # feature_flags.to_parquet('feature_flags.parquet')
    yield feature_flags


@pytest.fixture(scope="function")
def feature_flags_dataframe():
    """
    Fixture to create a feature flags fixture for unit testing
    """
    df = pd.DataFrame(data={"flag": ["season", "playoffs"], "is_enabled": [1, 0]})
    return df

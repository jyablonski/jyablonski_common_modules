import pandas as pd
import pytest
from sqlalchemy.exc import ProgrammingError

from jyablonski_common_modules.sql import write_to_sql


def test_write_to_sql(postgres_conn, shipping_data):
    table_name = "shipping_data"
    count_check = f"SELECT count(*) FROM sales_source.{table_name}"
    write_to_sql(postgres_conn, table_name, shipping_data, "replace")

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)
    assert count_check_results_after["count"][0] == 3


def test_write_to_sql_empty_df(postgres_conn, capfd):
    table_name = "shipping_data"
    fake_data = pd.DataFrame()

    write_to_sql(postgres_conn, table_name, fake_data, "replace")

    out, err = capfd.readouterr()
    assert out == f"{table_name} is empty, not writing to SQL\n"


def test_write_to_sql_fail(postgres_conn, shipping_data):
    table_name = "shipping_data2"
    bad_df = pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
    write_to_sql(postgres_conn, table_name, shipping_data, "replace")

    with pytest.raises(ProgrammingError):
        write_to_sql(postgres_conn, table_name, bad_df, "append")

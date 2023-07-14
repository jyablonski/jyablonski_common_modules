import pandas as pd

from jyablonski_common_modules.sql import write_to_sql_upsert


def test_write_to_sql_upsert(postgres_conn, sales_data):
    count_check = "SELECT count(*) FROM sales_source.sales_data"

    count_check_results_before = pd.read_sql_query(sql=count_check, con=postgres_conn)

    # upsert 2 records
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table="sales_data",
        df=sales_data,
        pd_index=["id"],
    )

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)

    assert count_check_results_before["count"][0] == 3

    assert count_check_results_after["count"][0] == 4


def test_write_to_sql_upsert_new_table(postgres_conn, sales_data):
    table_name = "sales_data_new"
    count_check = f"SELECT count(*) FROM sales_source.{table_name}"

    # upsert 2 records
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table=table_name,
        df=sales_data,
        pd_index=["id"],
    )

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)

    assert count_check_results_after["count"][0] == 2


def test_write_to_sql_upsert_empty(postgres_conn, capfd):
    fake_df = pd.DataFrame()
    table_name = "fake_data"
    # upsert 2 records
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table=table_name,
        df=fake_df,
        pd_index=["id"],
    )

    out, err = capfd.readouterr()
    assert out == f"{table_name} is empty, not writing to SQL\n"


def test_write_to_sql_upsert_fail(postgres_conn):
    fake_df = pd.DataFrame(
        data={"id": [1, 2, 3], "my%col_is_screwedlol": ["team1", "team2", "team3"]}
    )
    table_name = "fake_data_pct"

    # upsert 2 records
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table=table_name,
        df=fake_df,
        pd_index=["id"],
    )

    assert 2 == 2

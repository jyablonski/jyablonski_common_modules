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
        table_type="upsert",
        pd_index=["id"],
    )

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)

    assert count_check_results_before["count"][0] == 3

    assert count_check_results_after["count"][0] == 4

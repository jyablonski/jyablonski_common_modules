import pandas as pd

from jyablonski_common_modules.sql import write_to_sql


def test_write_to_sql(postgres_conn, shipping_data):
    count_check = "SELECT count(*) FROM sales_source.shipping_data"
    write_to_sql(postgres_conn, "shipping_data", shipping_data, "replace")

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)
    assert count_check_results_after["count"][0] == 3

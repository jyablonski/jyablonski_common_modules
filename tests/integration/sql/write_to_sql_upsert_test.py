import logging

import pandas as pd
import pytest

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
        primary_keys=["id"],
    )

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)

    assert count_check_results_before["count"][0] == 3

    assert count_check_results_after["count"][0] == 4

def test_write_to_sql_upsert_update_existing(postgres_conn, sales_data):
    sales_data.loc[sales_data["id"] == 2, "item"] = "Updated Sandals"
    
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table="sales_data",
        df=sales_data,
        primary_keys=["id"],
    )

    updated_record = pd.read_sql_query(
        sql="SELECT item FROM sales_source.sales_data WHERE id = 2",
        con=postgres_conn,
    )

    assert updated_record["item"][0] == "Updated Sandals"

def test_write_to_sql_upsert_composite_key(postgres_conn):
    composite_data = pd.DataFrame({
        "id": [1, 2],
        "item": ["Item1", "Item2"],
        "location": ["Warehouse1", "Warehouse2"],
        "price": [100, 200]
    })
    
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table="sales_data_composite",
        df=composite_data,
        primary_keys=["id", "location"],
    )
    
    result = pd.read_sql_query(
        sql="SELECT * FROM sales_source.sales_data_composite",
        con=postgres_conn,
    )

    assert len(result) == 2

def test_write_to_sql_upsert_conflict_handling(postgres_conn, sales_data):
    conflicting_data = pd.DataFrame({
        "id": [2], 
        "item": ["Updated Belt"], 
        "price": [200]
    })

    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table="sales_data",
        df=conflicting_data,
        primary_keys=["id"],
    )

    updated_record = pd.read_sql_query(
        sql="SELECT item, price FROM sales_source.sales_data WHERE id = 2",
        con=postgres_conn,
    )

    assert updated_record["item"][0] == "Updated Belt"
    assert updated_record["price"][0] == 200

def test_write_to_sql_upsert_new_table(postgres_conn, sales_data):
    table_name = "sales_data_new"
    count_check = f"SELECT count(*) FROM sales_source.{table_name}"

    # upsert 2 records
    write_to_sql_upsert(
        conn=postgres_conn,
        schema="sales_source",
        table=table_name,
        df=sales_data,
        primary_keys=["id"],
    )

    count_check_results_after = pd.read_sql_query(sql=count_check, con=postgres_conn)

    assert count_check_results_after["count"][0] == 2


def test_write_to_sql_upsert_empty(postgres_conn, caplog):
    fake_df = pd.DataFrame()
    table_name = "fake_data"

    with caplog.at_level(logging.INFO):
        write_to_sql_upsert(
            conn=postgres_conn,
            schema="sales_source",
            table=table_name,
            df=fake_df,
            primary_keys=["id"],
        )

    assert f"{table_name} is empty, skipping SQL upsert." in caplog.text


def test_write_to_sql_upsert_fail_exception(postgres_conn):
    fake_df = pd.DataFrame(
        data={"id": [1, 2, 3], "my%col_is_screwedlol": ["team1", "team2", "team3"]}
    )
    table_name = "fake_data_pct"
    
    with pytest.raises(ValueError):
        write_to_sql_upsert(
            conn=postgres_conn,
            schema="sales_source",
            table=table_name,
            df=fake_df,
            primary_keys=["fake_id"],
        )
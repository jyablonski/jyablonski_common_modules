import pytest
from sqlalchemy import exc

from jyablonski_common_modules.sql import sql_connection

def test_sql_connection_fail():
    with pytest.raises(exc.SQLAlchemyError):
        conn = sql_connection(
            database="my_fake_postgres",
            schema=1,
            user=1,
            pw=1,
            host="my_fake_ip",
        )
        conn.connect()
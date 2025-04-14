from datetime import date

import pytest

from jyablonski_common_modules.general import (
    construct_date_partition,
)
from jyablonski_common_modules.general.date_partitioning import _split_date_partition


@pytest.mark.parametrize(
    "date, expected_partition",
    [
        (date(2025, 1, 1), (2025, "01", "01")),
        (date(2025, 12, 31), (2025, "12", "31")),
        (date(2023, 10, 15), (2023, "10", "15")),
    ],
)
def test_split_date_partition(date, expected_partition):
    assert _split_date_partition(date) == expected_partition


@pytest.mark.parametrize(
    "date, expected_partition",
    [
        (date(2025, 1, 1), "year=2025/month=01/day=01"),
        (date(2025, 12, 31), "year=2025/month=12/day=31"),
        (date(2023, 10, 15), "year=2023/month=10/day=15"),
    ],
)
def test_construct_date_partition(date, expected_partition):
    assert construct_date_partition(date) == expected_partition

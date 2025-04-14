from datetime import date

from jyablonski_common_modules.general import get_leading_zeroes


def _split_date_partition(date: date) -> tuple[int, str, str]:
    """
    Internal Function to split a date into year, month, and day,
    with the month and day formatted with leading zeroes.

    Args:
        date (date): The date to split.

    Returns:
        tuple: A tuple containing the year, month, and day.
    """
    year = date.year
    month = get_leading_zeroes(month=date.month)
    day = get_leading_zeroes(month=date.day)
    return year, month, day


def construct_date_partition(date: date) -> str:
    """
    Function to construct a date partition string from a date.
    This is useful for partitioning data in a directory structure
    when writing files to S3 or similar storage systems.

    Args:
        date (date): The date to construct the partition string from.

    Returns:
        str: The date partition string in the format
            `"year={year}/month={month}/day={day}"`

    Raises:
        TypeError: If the date parameter is not a datetime.date object.

    Example:
        >>> date = datetime.date(2023, 10, 15)
        >>> construct_date_partition(date)
        'year=2023/month=10/day=15'
    """
    if not isinstance(date, date):
        raise TypeError("The date parameter must be a datetime.date object.")
    year, month, day = _split_date_partition(date=date)
    return f"year={year}/month={month}/day={day}"

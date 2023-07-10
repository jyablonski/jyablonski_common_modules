import os

from jyablonski_common_modules.logging import create_logger


def test_create_logger():
    log_file_location = "example.log"

    with open(log_file_location, "w") as fp:
        fp.write(f"1")

    logger = create_logger(
        log_file=log_file_location,
    )
    logger.info(f"hi")

    dir_list = os.listdir()
    assert log_file_location in dir_list

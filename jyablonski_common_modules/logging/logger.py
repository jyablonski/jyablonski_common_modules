import logging

from opensearch_logger import OpenSearchHandler


def create_logger(es_index: str, es_host_endpoint: str):
    """
    Logger which writes to both STDOUT as well as an Opensearch Endpoint

    Args:
        es_index (str): The name of the Opensearch Index that logs will go to.
            It will be automatically created if it doesn't already exist.

        es_endpoint (str): The Endpoint of the Opensearch Cluster
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )
    handler = OpenSearchHandler(
        index_name=es_index,
        hosts=[f"{es_host_endpoint}:443"],
        # http_auth=("admin", "admin"),
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

import logging


def configure_logging():
    """
    Configura el logger principal del backend.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger("always-beautiful-api")

    return logger
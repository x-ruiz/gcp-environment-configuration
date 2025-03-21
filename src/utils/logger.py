import logging


def get_logger(name, level=logging.DEBUG):
    """Returns a logger with the specified name and level."""
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)

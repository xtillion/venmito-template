import logging

def configure_logging():
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(filename)s - %(levelname)s:%(message)s', level=logging.INFO)
    return logger
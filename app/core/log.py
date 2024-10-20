import logging


def get_logger(log_level: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    return logger

import logging

DEBUG_COLOUR = '\033[94m'
INFO_COLOUR = '\033[32m'
WARNING_COLOUR = '\033[93m'
ERROR_COLOUR = '\033[91m'

# Set up logger
format = f'[%(levelname)s] %(asctime)s - %(message)s'
handler = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def set_colour_of_logger(colour):
    handler.setFormatter(logging.Formatter(colour + format))

def info(message):
    set_colour_of_logger(INFO_COLOUR)
    logging.info(str(message))
    set_colour_of_logger(DEBUG_COLOUR)

def warning(message):
    set_colour_of_logger(WARNING_COLOUR)
    logging.warning(str(message))
    set_colour_of_logger(DEBUG_COLOUR)

def error(message):
    set_colour_of_logger(ERROR_COLOUR)
    logging.error(str(message))
    set_colour_of_logger(DEBUG_COLOUR)

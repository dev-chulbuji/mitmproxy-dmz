import logging
import logging.handlers

logger = logging.getLogger('mitm')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./log/mitm-proxy.log')
logger.addHandler(file_handler)

def info(msg):
    logger.info(msg)

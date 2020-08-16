import logging
import os
import sys


def setup_logger(name, save_dir=None):
    logger = logging.getLogger(name)

    logger.propagate = False

    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if save_dir:
        fh = logging.FileHandler(os.path.join(save_dir, 'log.txt'), mode='a')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

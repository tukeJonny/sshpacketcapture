#-*- coding: utf-8 -*-
import logging

def get_logger(name, fpath=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if fpath is None:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
    else:
        handler = logging.FileHandler(fpath, mode='w')
        handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

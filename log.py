#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import time
import os


def init_log(filename):
    # mon_str = time.strftime('%Y-%m',time.localtime(time.time()))
    log_folder = "./log/"

    if os.path.exists(log_folder) == False:
        os.makedirs(log_folder)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(process)d][%(filename)s:%(lineno)s]::%(message)s')

    # notice log
    log_file_name = log_folder + filename
    hdlr = logging.handlers.TimedRotatingFileHandler(log_file_name,when='H',interval=1,backupCount=240)
    # hdlr = logging.FileHandler(log_file_name)
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.NOTSET)
    hdlr.suffix = "%Y-%m-%d-%H"

    # warning log
    wlog_file_name = log_file_name + '.wr'
    whdlr = logging.handlers.TimedRotatingFileHandler(wlog_file_name,when='H',interval=1,backupCount=240)
    # whdlr = logging.FileHandler(wlog_file_name)
    whdlr.setFormatter(formatter)
    whdlr.setLevel(logging.WARNING)
    whdlr.suffix = "%Y-%m-%d-%H"

    logger = logging.getLogger()
    logger.addHandler(hdlr)
    logger.addHandler(whdlr)
    logger.setLevel(logging.INFO)

    return logger



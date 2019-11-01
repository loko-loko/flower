#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

from loguru import logger

def logger_filter(args):

    def filter(record):
        if '|Exit|' in record["message"]:
            logger.info(f"o-> Script Exit <-o")
            sys.exit()

        if args.silent:
            if re.search('\[\*\]|\|Exit\|', record["message"]):
                return record
        else:            
            return record            
    
    return filter    

def logger_init(args, log_path):

    level = "DEBUG" if args.debug else "INFO"

    if not os.path.exists(log_path):
        os.makedirs(log_path)      

    log_file = os.path.join(log_path, 'flower.log')

    logger.remove()
    logger.add(
        sys.stderr, level=level, filter=logger_filter(args),
        format="{time:YYYY/MM/DD HH:mm:ss}  {level:<7} - {message}"
    )

    if not args.no_log and not args.debug:
        logger.add(log_file, rotation="2 MB")

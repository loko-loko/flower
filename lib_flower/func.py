#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint, pformat
from subprocess import Popen, PIPE, STDOUT

from loguru import logger

# Command #
   
def cmd_exec(cmd, wait=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cmd_return=False):
    
    logger.debug(f'[Command] {cmd}')
    
    popen = Popen(
        cmd,
        shell=True,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        encoding='utf-8'
    )
    
    if wait and popen.wait() != 0:
        logger.debug(f'[Command] Return : {pformat(popen.stdout.readlines())}')
        logger.error(f'[Command] Problem : {cmd} |Exit|')
        
    if cmd_return:
        return popen.stdout.readlines()

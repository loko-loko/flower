#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import argparse
from sys import stderr

from loguru import logger as log

from jeedom_flower_spray.jeedom_api import JeedomApi
from jeedom_flower_spray.utils import get_config
from jeedom_flower_spray.utils import get_moisture_from_exporter


# Default vars
LOG_PATH = "/var/log/jeedom-flower-spray"
SPRAY_TIME = 20
MIN_MOISTURE_LEVEL = 18
JEEDOM_START_ID = 1
JEEDOM_STOP_ID = 2


def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Config file"
    )
    parser.add_argument(
        "--log-path",
        default=LOG_PATH,
        help=f"Log path [Default: {LOG_PATH}]"
    )
    parser.add_argument(
        "--spray-time",
        help=f"Time of water spray [Default: {SPRAY_TIME}]",
        default=SPRAY_TIME
    )
    parser.add_argument(
        "--min-moisture-level",
        help=f"Level of min moisture for spray [Default: {MIN_MOISTURE_LEVEL}]",
        default=MIN_MOISTURE_LEVEL
    )
    parser.add_argument(
        "--jeedom-start-id",
        help=f"Jeedom scenario ID to start spray [Default: {JEEDOM_START_ID}]",
        default=JEEDOM_START_ID
    )
    parser.add_argument(
        "--jeedom-stop-id",
        help=f"Jeedom scenario ID to stop spray [Default: {JEEDOM_STOP_ID}]",
        default=JEEDOM_STOP_ID
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Enable writing logs to a file"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Debug Mode"
    )
    return parser.parse_args()


def main():
    # Argument Parse/Check #
    args = arg_parser()
    # Init logger
    log_level = "DEBUG" if args.debug else "INFO"
    formatter="{time:YYYY/MM/DD HH:mm:ss}  {level:<7} - {message}"
    log.remove()
    log.add(
        stderr,
        level=log_level,
        format=formatter
    )
    if args.logs:
        if not os.path.exists:
            log.error(f"[log] No path found from {args.log_path}")
            exit(1)
        log_file = os.path.join(args.log_path, "spray.log")
        log.add(
            log_file,
            level=log_level,
            format=formatter,
            rotation="5 MB"
        )

    log.info("[jeedom-flower-spray] ** Starting **")
    # Load Config File #
    config = get_config(args.config) 
    # Get moisture from exporter
    moisture_levels = get_moisture_from_exporter(
        url=config["exporter_url"],
        flowers=config["flowers"]
    )
    # Comparing current moisture levels with defined limit
    if any([current_level <= args.min_moisture_level for current_level in moisture_levels]):
        # Initialize Jeedom api
        jeedom = JeedomApi(
            host=config["jeedom_ip"],
            api_key=config["jeedom_api_key"]
        )
        # Spray execution
        log.warning(f"[moisture] Level too low. Spray execution ..")
        jeedom.spray_execution(
            start_id=args.jeedom_start_id,
            stop_id=args.jeedom_stop_id,
            spray_time=args.spray_time
        )

    else:
        log.info("[moisture] Level OK")

    log.info("[jeedom-flower-spray] ** Finish **")

if __name__ == "__main__":
    main()


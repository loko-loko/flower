#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from loguru import logger as log

from jeedom_flower_watering.utils import get_config
from jeedom_flower_watering.utils import check_config_options
from jeedom_flower_watering.exporter import get_moisture_from_exporter
from jeedom_flower_watering.logger import logger_initialization
from jeedom_flower_watering.watering import check_moisture_levels
from jeedom_flower_watering.watering import watering_execution


# Default vars
LOG_PATH = "/var/log/jeedom-flower-watering"
WATERING_TIME = 20
MIN_MOISTURE_LEVEL = 20

# Default config
# NOTE: if None there is no default value
DEFAULT_CONFIG = {
    "exporter_url": "http://127.0.0.1:9250",
    "jeedom_start_id": 1,
    "jeedom_stop_id": 2,
    "jeedom_ip": None,
    "jeedom_api_key": None,
    "flowers": None
}

def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
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
        "--watering-time",
        help=f"Time of watering in seconds [Default: {WATERING_TIME}]",
        default=WATERING_TIME,
        type=int
    )
    parser.add_argument(
        "--moisture-level-limit",
        help=f"Level of min moisture for watering [Default: {MIN_MOISTURE_LEVEL}]",
        default=MIN_MOISTURE_LEVEL,
        type=int
    )
    parser.add_argument(
        "--only-watering",
        action="store_true",
        help="Run only watering, without check of moisture level"
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Enable writing logs to a file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug Mode"
    )
    return parser.parse_args()


def main():
    # Argument Parse/Check #
    args = arg_parser()
    # Init logger
    logger_initialization(
        log_path=args.log_path,
        log_file="watering.log",
        write_to_file=args.logs,
        debug=args.debug
    )
    # Starting tool
    level_status = False
    log.info(
        "[flower-watering] Starting. "
        f"Watering Time: {args.watering_time}s, "
        f"Moisture Limit: {args.moisture_level_limit}"
    )
    # Load Config File #
    config = get_config(args.config)
    config = check_config_options(
        config=config,
        defaults=DEFAULT_CONFIG
    )

    if not args.only_watering:
        # Get moisture from exporter
        moisture_levels = get_moisture_from_exporter(
            url=config["exporter_url"],
            flowers=config["flowers"]
        )
        # Comparing current moisture levels with defined limit
        level_status = check_moisture_levels(
            levels=moisture_levels,
            level_limit=args.moisture_level_limit
        )

    if args.only_watering or level_status:
        # Start watering
        watering_execution(
            config=config,
            watering_time=args.watering_time
        )

if __name__ == "__main__":
    main()


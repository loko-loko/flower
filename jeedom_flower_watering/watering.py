from loguru import logger as log

from jeedom_flower_watering.jeedom_api import JeedomApi


def check_moisture_levels(levels, level_limit):
    # Comparing current moisture levels with defined limit
    if any([level <= level_limit for level in levels]):
        log.warning(f"[moisture] Level too low. Current: {levels}, Limit: {level_limit}")
        return True
    log.info("[moisture] Level OK")
    return False


def watering_execution(config, watering_time):
    # Initialize Jeedom api
    jeedom = JeedomApi(
        host=config["jeedom_ip"],
        api_key=config["jeedom_api_key"]
    )
    # Watering execution
    jeedom.watering_execution(
        start_id=config["jeedom_start_id"],
        stop_id=config["jeedom_stop_id"],
        watering_time=watering_time
    )
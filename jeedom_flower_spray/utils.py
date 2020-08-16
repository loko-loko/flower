import re

import requests
from loguru import logger as log
from yaml import safe_load

 
def get_config(conf_file):
    log.debug(f"[config] Get data from: {conf_file}")
    try:
        with open(conf_file) as f:
            data = safe_load(f)
        return data["configs"]
    except FileNotFoundError as e:
        log.error(f"[config] File not found: {e}")
        exit(1)
    except Exception as e:
        log.error(f"[config] File cannot be parsed: {e}")
        exit(1)


def get_moisture_from_exporter(url, flowers):
    log.info(f"[exporter] Get moisture level from {url}")
    log.debug(f"[exporter] Flower(s) to collect: {flowers}")
    # Get data from mi flower exporter
    request = requests.get(url)
    moisture_levels = []
    for flower in flowers:
        re_pattern = re.compile(f"mi_flower_moisture.*name=\"{flower}\".*")
        for line in request.text.split("\n"):
            if not re_pattern.search(line):
                continue
            # Get moisture level for current flower
            moisture_level = float(line.split()[-1])
            log.info(f"[exporter] Current moisture level for {flower}: {moisture_level}")
            moisture_levels.append(moisture_level)

    if not moisture_levels:
        log.error(f"[exporter] No moisture levels found for {config['flowers']}. ABORD")
        exit(1)

    return moisture_levels


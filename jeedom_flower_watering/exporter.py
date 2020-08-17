import re

import requests
from loguru import logger as log


def get_moisture_from_exporter(url, flowers):
    log.info(f"[exporter] Get moisture level from {url}")
    log.debug(f"[exporter] Flower(s) to collect: {flowers}")
    # Get data from mi flower exporter
    try:
        request = requests.get(url)
    except Exception as e:
        log.error(f"[exporter] Problem during request from {url}")
        exit(1)
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
        log.error(f"[exporter] No moisture levels found for {flowers}. ABORD")
        exit(1)

    return moisture_levels
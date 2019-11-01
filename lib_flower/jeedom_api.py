#!/usr/bin/env python3

import time
import requests

from loguru import logger

class JeedomApi():

    def __init__(self, host, key):
        self.host = host
        self.key = key
        self.endpoint = self.get_endpoint()
        
    def get_endpoint(self):
        return f'http://{self.host}/core/api/jeeApi.php?apikey={self.key}'
        
    def start_scenario(self, id, name):
        logger.info(f"[Jeedom] Execution : {name} [{id}]")
        request = f'{self.endpoint}&type=scenario&id={id}&action=start'
        result = requests.get(request)
        
        return result
        
    def launch_water_scenario(self, id_start, id_end, wait_time=20):
        self.start_scenario(id_start, 'Water Start')
        logger.debug(f'Wait : {wait_time}')
        time.sleep(wait_time)
        self.start_scenario(id_end, 'Water Stop')
        

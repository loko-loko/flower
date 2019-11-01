#!/usr/bin/env python3

import re

from pprint import pformat

from loguru import logger

from btlewrap import available_backends, BluepyBackend, GatttoolBackend, PygattBackend
from .miflora import miflora_scanner
from .miflora.miflora_poller import *

class FlowerInfo(object):
    
    def __init__(self, name, mac):
        
        self.name = name
        self.mac = mac.upper()
        self.backend = GatttoolBackend
        
        self.check_mac()
        
    def check_mac(self):
        if not re.search(r'^C4:7C:8D(:[0-9A-F]{2}){3}$', self.mac):
            logger.error('[Flower] The MAC address "{self.mac}" seems to be in the wrong format')
            raise Exception(f'The MAC address "{self.mac}" seems to be in the wrong format')
        
    def poll(self):
        """Poll data from the sensor."""
        
        logger.info(f'[Flower] Getting data from {self.name} [{self.mac}]')
        
        try:
            poller = MiFloraPoller(self.mac, self.backend)
        
        except:
            raise Exception(f'Getting data error from {self.name}')
        
        self.data = {
            'name': self.name,
            'temperature': float(poller.parameter_value(MI_TEMPERATURE)),
            'moisture': int(poller.parameter_value(MI_MOISTURE)),
            'light': int(poller.parameter_value(MI_LIGHT)),
            'conductivity': int(poller.parameter_value(MI_CONDUCTIVITY)),
            'battery': int(poller.parameter_value(MI_BATTERY)),
            'collect_date': str(datetime.now()),
        }
        
        logger.debug('[Flower] Data : {0}'.format(pformat(self.data)))

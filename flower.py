#!/usr/bin/env python3

#================================================================================#
# ------------------------------- IMPORT LIBRARY ------------------------------- #
#================================================================================#

import os
import time
import argparse
from pprint import pprint, pformat

import yaml
from loguru import logger

from lib_flower.logger import logger_init
from lib_flower.jeedom_api import JeedomApi
from lib_flower.flower import FlowerInfo
from lib_flower.database import FlowerDataBase
  
def args_parse():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-c', '--config-file', help='Config file', required=True) 

    parser.add_argument('--new-env', action="store_true", help='New Virtual ENV')
    parser.add_argument('--debug', action="store_true", help='Debug Mode')
    parser.add_argument('--silent', action="store_true", help='Silent Mode')
    parser.add_argument('--db-write', action="store_true", help='Write Data on DB')
    parser.add_argument('--no-log', action="store_true", help='No Output File Log')
    
    parser.add_argument('--spray', action="store_true", help='Water Spray Flower')
    parser.add_argument('--spray-time', help='Time of Water Spray', default=20)
    parser.add_argument('--water-level', help='Level of Min Water for Spray', default=18)
    parser.add_argument('--start-id', help='Jeedom Scenario ID to Start Spray', default=1)
    parser.add_argument('--stop-id', help='Jeedom Scenario ID to Stop Spray', default=2)
    
    return parser.parse_args()


def load_config(conf_file):
   
    if not os.path.exists(conf_file):
        logger.error(f'Config file : {conf_file} not find')
 
    with open(conf_file, 'r') as f:
        try:
            return yaml.safe_load(f)

        except yaml.YAMLError as e:
            logger.error(f'Yaml config error : {e}')

def main():
    
    # Global Var #
    
    PYTHON_BIN = '/usr/bin/python3'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    LOG_PATH = os.path.join(BASE_DIR, 'logs')
    REQUIREMENTS_F = os.path.join(BASE_DIR, 'requirements.txt')

    # Argument Parse/Check #
    
    args = args_parse()
 
    # Init logger #
   
    logger_init(args, LOG_PATH)

    # Load Config File #

    conf_data = load_config(args.config_file) 
  
    # Init Script #
    
    start_time = time.time()
    
    logger.info('[Script] o-> Flower Exec Start <-o')
    
    # Get Config Info #
    
    db_infos = conf_data['db_infos']
    host_infos = conf_data['host_infos']
    flower_infos = conf_data['flower_infos']
    jeedom_ip = conf_data['jeedom_ip']
    jeedom_api_key = conf_data['jeedom_api_key']
    
    for name, f_infos in flower_infos.items():
        
        if f_infos['active']:
            
            try:
                flower = FlowerInfo(name, f_infos['mac'])
                flower.poll()
                
            except:
                logger.error(f'Collect abord for flower {name}')
                continue
            
            f_infos['data'] = flower.data
     
    if args.db_write:
    
        for type, h_infos in host_infos.items():
            
            db_infos['host'] = h_infos['address']
            db_infos['sslmode'] = 'require'
            
            if h_infos['local']:
                del db_infos['sslmode']
            
            flower_db = FlowerDataBase(db_infos, flower_infos)
            flower_db.db_connect()
            flower_db.send_data()
            flower_db.close()
        
        logger.info(f'[Database][*] Data send with success')
        
    else:
        logger.info(pformat(flower_infos))
        
    if args.spray:
        spray_exec = JeedomApi(jeedom_ip, jeedom_api_key)
        
        moisture_levels = (
            [f['data']['moisture'] for f in flower_infos.values() if f.get('data')]
        )
        
        if any([m <= args.water_level for m in moisture_levels]):
            logger.warning(f'[Jeedom][*] Water level too Low {moisture_levels}. Spray ..')
            spray_exec.launch_water_scenario(
                args.start_id, args.stop_id, args.spray_time
            )
        
        else:
            logger.info(f'[Jeedom][*] Water level OK {moisture_levels}')
            
    exec_time = time.strftime(
        "%H:%M:%S",
        time.gmtime((time.time() - start_time))
    )
    
    logger.info(f"[Script] o-> End ({exec_time}) <-o")
    
if __name__ == '__main__':
    main()

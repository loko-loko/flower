#!/usr/bin/env python3

import json
import psycopg2

from pprint import pformat

from loguru import logger

class FlowerDataBase(object):
    
    def __init__(self, db_infos, flower_infos):
        
        self.db_infos = db_infos
        self.flower_infos = flower_infos
        
        self.datas = self.get_data_flowers()
        
    def get_data_flowers(self):
        
        return [f['data'] for f in self.flower_infos.values() if f.get('data')]
        
    def db_connect(self):
        
        logger.debug(f'[Database] Credential : {pformat(self.db_infos)}')
        logger.info(
            f'[Database] Connect : {self.db_infos["dbname"]} [{self.db_infos["host"]}]'
        )
        
        try:
            self.conn = psycopg2.connect(**self.db_infos)
            self.cur = self.conn.cursor()
            
        except:
            logger.error('[Database] Unable to connect database')
            raise Exception('Unable to connect database')
        
        
    def send_data(self):
        
        logger.info(
            f'[Database] Send data : {self.db_infos["dbname"]} [{self.db_infos["host"]}]'
        )
        
        for data in self.datas:
            key_lst = data.keys()
            val_lst = [data[k] for k in key_lst]
            
            self.cur.execute(
                f'INSERT INTO flower_flower ({",".join(key_lst)})'
                f'VALUES ({",".join(["%s"] * len(key_lst))})',
                val_lst
            )
            
            self.conn.commit()
        
    def close(self):
        self.cur.close()
        self.conn.close()
        

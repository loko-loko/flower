import os
from shutil import rmtree

from loguru import logger

from .func import cmd_exec

class VirtualEnv():
    
    def __init__(self, base_dir, python_bin, pip_req_file, venv_name='venv'):
    
        self.base_dir = base_dir
        self.python_bin = python_bin
        self.pip_req_file = pip_req_file
        self.venv_name = venv_name
        
        self.venv_dir = os.path.join(self.base_dir, self.venv_name)
        
    def check_venv(self):
        
        return True if os.path.exists(self.venv_dir) \
            else False
        
    def create_venv(self, new_venv):
        
        if new_venv:
            self.delete_venv()
        
        if not self.check_venv():
            logger.info(f'[V.Env] Creation : {self.venv_dir}')
            cmd_exec(logger, f'{self.python_bin} -m virtualenv {self.venv_dir}')
            
            logger.info('[V.Env] Installation of PIP Requirements')
            cmd_exec(logger, f'{self.venv_dir}/bin/python -m pip install -r {self.pip_req_file}')

        
    def activate_venv(self):
        
        logger.info(f'[V.Env] Activation : {self.venv_dir}')
        
        try:
            os.chdir(self.venv_dir)
            activate_script = os.path.join(self.venv_dir, 'bin', 'activate_this.py')
            exec(open(activate_script).read(), dict(__file__=activate_script))
        
        except:
            logger.error('[V.Env] Activation Problem |Exit|')

        os.chdir(self.base_dir)
        
        
    def delete_venv(self):

        if os.path.exists(self.venv_dir):
            logger.info(f'[V.Env] Delete : {self.venv_dir}')
            rmtree(self.venv_dir)
            
        else:
            logger.warning(f'[V.Env] Not Find : {self.venv_dir}')

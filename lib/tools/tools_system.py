# coding: utf-8

import os
import sys
import multiprocessing


class Tools_system():

    def get_env(self, SCRenv):
        SCRenv['exec'] = sys.executable
        
        if 'chain' in set(sys.argv):
            SCRenv['flag'] = 'chain'
        return SCRenv

    def cpu_count(self):
        return multiprocessing.cpu_count()

    def pwd(self):
        return os.getcwd()
# coding: utf-8

import os
import json
#import psutil
import subprocess
import collections
import signal

import config as CONF
from lib.tools.s_logger import S_logger

class Tools_receive():

    def delete_schedule(self, SCRschedule, sr):
        for sc_index in range(len(SCRschedule)):
            if(
                SCRschedule[sc_index]['sec'] == sr['sec'] and
                SCRschedule[sc_index]['d']['file_path'] == sr['d']['file_path'] and
                SCRschedule[sc_index]['d']['file_name'] == sr['d']['file_name']
            ):
                SCRschedule.pop(sc_index)
                return SCRschedule
        return SCRschedule
    
    def conf_local(self, sr):
        CONF.SCR['module'] = 'WSGI'
        slog = S_logger(SCRenv=CONF.SCR)
        data = sr['d']['data_key']
        try:
            with open('code/' + sr['d']['file_path'] + '/local_conf.py', 'w') as f:
                f.write('CONF = ' + json.dumps(data, indent=4))
        except:
            slog.output(lv='WARN', log='can\'t create local_conf.py. check to folder name.')
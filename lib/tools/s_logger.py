# coding: utf-8

import os
import sys
import logging
import traceback

import config as CONF

class S_logger:

    def __init__(self, SCRenv):
        log_path = SCRenv['logger']['path'] + SCRenv['module'] + '.log'
        if(SCRenv['logger']['write_mode'] == 'w' and SCRenv['module'] == 'SCR'):
            for fn in ['SCR', 'SUB', 'GUI', 'WS']:
               if(os.path.exists(SCRenv['logger']['path'] + fn + '.log')):
                    os.remove(SCRenv['logger']['path'] + fn + '.log')
        if(not os.path.exists(log_path) and SCRenv['logger']['write_mode'] == 'a'):
            with open(log_path, "w", encoding="UTF-8") as f:
                pass
        self.log_path = log_path
        self.write_mode = SCRenv['logger']['write_mode']
        self.level = SCRenv['logger']['level']
        self.console_stream = SCRenv['logger']['console_stream']
        self.log_file_out = SCRenv['logger']['log_file_out']
        self.roll = SCRenv['module']

    def output(self, lv, log, tb=[]):
        
        if(50 <= self.level):
            return
        elif(lv == "CRITICAL" and self.level < 50):
            log_output_c = '\033[31mCRITICAL\033[0m '
            log_output_f = 'CRITICAL'
        elif(lv == "ERROR" and self.level < 40):
            log_output_c = '\033[31mERROR\033[0m '
            log_output_f = 'ERROR'
        elif(lv == "WARN" and self.level < 30):
            log_output_c = '\033[33mWARN\033[0m '
            log_output_f = 'WARN'
        elif(lv == "INFO" and self.level < 20):
            log_output_c = '\033[32mINFO\033[0m '
            log_output_f = 'INFO'
        elif(lv == "DEBUG" and self.level < 10):
            log_output_c = '\033[35mDEBUG\033[0m '
            log_output_f = 'DEBUG'
        else:
            log_output_c = '\033[35mNOTSET\033[0m '
            log_output_f = 'NOTSET'

        log_mes = '[' + self.roll + '] '

        if(sys.exc_info()[0] != None):
            except_str = sys.exc_info()[0].__name__
            t, v, tb = sys.exc_info()
            trackback_list = traceback.format_exception(t,v,tb)
            log_mes += 'except:' + except_str + ' '
        else:
            trackback_list = tb

        if(sys._getframe(1).f_code.co_name != '<module>'):
            log_mes += 'in ' + sys._getframe(1).f_code.co_name + ' '
        log_mes += '> ' + log

        if(self.console_stream[log_output_f]):
            print(log_output_c + log_mes)
        if(self.log_file_out[log_output_f]):
            with open(self.log_path, 'a') as f:
                f.write(log_output_f + ' ' + log_mes + '\n')
                if(len(trackback_list) != 0):
                    f.write('--track-back---------------------------------' + '\n')
                    f.write('\n'.join(trackback_list))
                    f.write('---------------------------------------------' + '\n')
        return


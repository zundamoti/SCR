# coding: utf-8

from lib.tools.tools_data import Tools_data
from lib.tools.tools_file import Tools_file
from lib.tools.tools_receive import Tools_receive
from lib.tools.s_logger import S_logger

class Second:

    def task_check(self, SCRfield, SCRenv, SCRtasks):
        t_d = Tools_data()
        t_f = Tools_file()
        t_r = Tools_receive()
        SCRenv['befor'] = SCRenv['now']

        SCRschedule = t_d.get_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sc')
        if(SCRschedule != False):
            for ss in SCRschedule:
                if (ss['days1'] and ss['sec'] == SCRenv['now']) or SCRenv['now'] % ss['sec'] == 0:
                    tss = {}
                    tss['d'] = ss['d']
                    SCRenv['max_tid'] += 1
                    tss['tid'] = SCRenv['max_tid']
                    tss['sub_id'] = -1
                    SCRtasks.append(tss)

        SCRreceive = t_d.pop_receive_data(SCRfield=SCRfield, SCRenv=SCRenv)
        if(SCRreceive != False):
            for sr in SCRreceive:

                if('c' in sr):
                    if(sr['c'] != ''):
                        if(sr['c'] == 'delete_schedule'):
                            t_r.delete_schedule(SCRschedule=SCRschedule, sr=sr)
                        elif(sr['c'] == 'restart'):
                            SCRenv['flag'] = 'restart'
                        elif(sr['c'] == 'exit'):
                            SCRenv['flag'] = 'exit'
                        elif(sr['c'] == 'local_conf'):
                            t_r.conf_local(sr=sr)

                if('sec' in sr):
                    if(sr['sec'] == 0):
                        if('d' in sr):
                            tsr = {}
                            tsr['d'] = sr['d']
                            SCRenv['max_tid'] += 1
                            tsr['tid'] = SCRenv['max_tid']
                            tsr['sub_id'] = -1
                            SCRtasks.append(tsr)
                    else:
                        SCRschedule.append(sr)
        
        SCRcodes = t_f.get_codes()
        if(0 < len(SCRcodes)):
            t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='co', data=SCRcodes)

        t_d.truncate_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='ta')
        if(0 < len(SCRtasks)):
            t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='ta', data=SCRtasks)
        
        t_d.truncate_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sc')
        if(0 < len(SCRschedule)):
            t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sc', data=SCRschedule)

        t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='en', data=SCRenv)
        t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='fi', data=SCRfield)

        return SCRenv, SCRtasks
# coding: utf-8

import os
#import psutil
import subprocess
import collections
import signal

from lib.tools.s_logger import S_logger

class Tools_process():

    def get_child_pid(self, SCRenv):
        cmd = ['ps ho pid --ppid=' + str(os.getpid())]
        spp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        ps_list = [ int(line.decode()) for line in spp.stdout ]
        exclude = 1
        if(SCRenv['i']['wsgi_server_popen'].pid in ps_list):
            exclude += 1
        if(SCRenv['i']['websocket_server_popen'].pid in ps_list):
            exclude += 1
        return ps_list, exclude

    def empty_sub(self, SCRenv, SCRtasks, tempSCRtasks):
        tn = ( [ i for i in range(SCRenv['max_sub_process']) ] 
        + [ t['sub_id'] for t in SCRtasks ]
        + [ tt['sub_id'] for tt in tempSCRtasks ] )
        counter = collections.Counter(tn)
        sub_id = counter.most_common()[-1][0]
        if(sub_id == -1):
            return 0
        return sub_id

    def need_wake_sub(self, SCRenv, SCRtasks, running_sub):
        tl = set( [ i['sub_id'] for i in SCRtasks] )
        if len(running_sub) == 0:
            return tl
        else:
            nws = set()
            for sn in range(SCRenv['max_sub_process']):
                if SCRenv['sub_state'][sn] not in running_sub and sn in tl:
                    nws.add(sn)
            return nws

    def start_sub(self, SCRenv, start_sub):
        #print(start_sub)
        for ss in start_sub:
            cmd = [SCRenv['python'], "scr_sub.py", str(ss)]
            spp = subprocess.Popen(cmd)
            SCRenv['sub_state'][ss] = spp.pid
        return SCRenv


    def run_server(self, SCRenv):
        if(SCRenv['gui']):

            cmd = [SCRenv['exec'], "scr_wsgi.py"]
            SCRenv['i']['wsgi_server_popen'] = subprocess.Popen(cmd)

            cmd = [SCRenv['exec'], "scr_websocket.py"]
            SCRenv['i']['websocket_server_popen'] = subprocess.Popen(cmd)

        return SCRenv

    def kill_process(self, pid):
        os.kill(pid, signal.SIGTERM)

    #def existence_ppid(self):
    #    p = psutil.Process(os.getppid())
    #    if p.status() == 'running':
    #        return True
    #    else:
    #        return False

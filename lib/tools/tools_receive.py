# coding: utf-8

import os
#import psutil
import subprocess
import collections
import signal

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
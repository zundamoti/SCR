#!/usr/bin/env python3
# coding: utf-8

import sys
import subprocess

from lib.setup import Setup
from lib.tools.tools_data import Tools_data
from lib.tools.tools_process import Tools_process
from lib.tools.s_logger import S_logger


def scr_sub(my_id):
    t_d = Tools_data()
    setup = Setup()

    SCRfield = setup.field()
    SCRenv = setup.env(SCRfield=SCRfield, roll='SUB')

    SCRtasks = t_d.get_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='ta')
    SCRspe = t_d.get_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sp')
    if(SCRspe):
        SCRspe = []
    MYtasks = [ t for t in SCRtasks if str(t['sub_id'])==my_id ]

    for task in MYtasks:
        if str(task['tid']) not in SCRspe:
            cmd = task['d']['lang'] + ' code/' + task['d']['file_path'] + '/' + task['d']['file_name']
            try:
                sp_run = subprocess.run(
                    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                SCRenv['log'].output(
                    lv='WARN', log='my_id=' + my_id + ' tid=' + str(task['tid']) + ' ' + task['d']['file_name'] + ' is CalledProcessError task cancel.')
            except subprocess.SubprocessError:
                SCRenv['log'].output(
                    lv='WARN', log='my_id=' + my_id + ' tid=' + str(task['tid']) + ' ' + task['d']['file_name'] + ' is SubprocessError task cancel.')
            except:
                SCRenv['log'].output(
                    lv='WARN', log='my_id=' + my_id + ' tid=' + str(task['tid']) + ' ' + task['d']['file_name'] + ' is error task cancel.')
            
            if(sp_run.returncode == 0):
                SCRenv['log'].output(
                    lv='INFO', log='my_id=' + my_id + ' tid=' + str(task['tid']) + ' ' + task['d']['file_name'] + ' is successful completion.')
            elif(sp_run.returncode == 1):
                trackback = [i for i in sp_run.stderr.decode().split('\n')]
                except_mes = trackback[len(trackback) - 2].split(':')[0]
                SCRenv['log'].output(
                    lv='WARN', log='my_id=' + my_id + ' tid=' + str(task['tid']) + ' ' + task['d']['file_name'] + ' except:' + except_mes + ' exit 1 task cancel.', tb=trackback)

            t_d.insert_spe(SCRfield=SCRfield, SCRenv=SCRenv, data=task['tid'])


if len(sys.argv) != 0:
    scr_sub(my_id=sys.argv[1])
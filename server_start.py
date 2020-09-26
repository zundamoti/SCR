#!/usr/bin/env python3
# coding: utf-8

from lib.setup import Setup
from lib.rotation import Rotation
from lib.second import Second

def scr():
    setup = Setup()
    rotation = Rotation()
    second = Second()
    print('>>> SCR start >>>')
    while True:
        SCRfield = setup.field()
        SCRenv = setup.env(SCRfield=SCRfield, roll='SCR')
        SCRtasks = setup.tasks(SCRfield=SCRfield, SCRenv=SCRenv)
        while True:
            SCRenv, SCRtasks = rotation.task_run(
                SCRfield=SCRfield, SCRenv=SCRenv, SCRtasks=SCRtasks)
            if SCRenv['befor'] != SCRenv['now']:
                SCRenv, SCRtasks = second.task_check(
                    SCRfield=SCRfield, SCRenv=SCRenv, SCRtasks=SCRtasks)
                if SCRenv['flag'] != 'none':
                    if SCRenv['flag'] == "restart":
                        print('>>> SCR restart >>>')
                        break
                    if SCRenv['flag'] == "exit":
                        setup.shut_down(SCRenv=SCRenv)

if __name__ == "__main__":
    scr()
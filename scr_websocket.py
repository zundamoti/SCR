#!/usr/bin/env python3
# coding: utf-8

import asyncio
import websockets
import time
import json

import config as CONF
from lib.setup import Setup
from lib.controller import Controller
from lib.tools.s_logger import S_logger
from copy import copy


async def start(websocket, path):
    ctrl = Controller()
    setup = Setup()

    p_rate = CONF.GUI['web_socket_pulse_rate']
    w_rate = CONF.GUI['web_socket_wait_rate']

    SCRfield = setup.field()
    SCRenv = setup.env(SCRfield=SCRfield, roll='WS')
    
    GUIraw = copy(CONF.GUI['GUIraw'])
    SCRenv['log'].output(lv='INFO', log='new conection.')
    
    try:
        while True:
            time.sleep(p_rate)
            send_json, GUIraw = ctrl.websocket_chaser(
                SCRfield=SCRfield, GUIenv=SCRenv, GUIraw=GUIraw)
            if(len(send_json.keys()) == 0):
                time.sleep(w_rate)
                await websocket.send('check')
            else:
                await websocket.send(json.dumps(send_json))
    except websockets.exceptions.ConnectionClosedError:
        SCRenv['log'].output(lv='INFO', log='close conection.')
        GUIraw = {}

CONF.SCR['module'] = 'WS'
slog = S_logger(SCRenv=CONF.SCR)

try:
    start_server = websockets.serve(
        start, CONF.GUI['address'], CONF.GUI['web_socket_port'])
    asyncio.get_event_loop().run_until_complete(start_server)
    slog.output(lv='INFO', log='Serving websocket-gui server on ' + CONF.GUI['address'] + ':' + str(CONF.GUI['web_socket_port']) + '...')
    asyncio.get_event_loop().run_forever()
except OSError:
    slog.output(lv='WARN', log='can\'t serve websocket server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['web_socket_port']) + ' already in use')
except KeyboardInterrupt:
    slog.output(lv='INFO', log='close websocket server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['web_socket_port']))

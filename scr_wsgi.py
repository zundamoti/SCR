#!/usr/bin/env python3
# coding: utf-8
# solveig code 

import os
import sys
import json
import urllib
from wsgiref import simple_server

from lib.setup import Setup
from lib.controller import Controller
from lib.tools.s_logger import S_logger
from lib.tools.tools_data import Tools_data
import config as CONF
 

def api_index(env):
    status = '200 OK'
    with open('wsgi/index.html') as f:
        text = f.read()
    print(type(text))
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    return status, headers, [t.encode("utf-8") for t in text.split('\n')]

#/rest/get_scr/sc/
def api_rest(env):
    g_c = Controller()
    json = g_c.get_json(path=env['PATH_INFO'])
    print(type(json))
    status = '200 OK'
    headers = [('Content-Type', 'text/json; charset=utf-8')]
    return status, headers, [bytes(json, encoding='utf-8')]

def api_receive(env):
    #g_c = Controller()
    #g_c.receive(env.json)
    t_d = Tools_data()
    setup = Setup()

    SCRfield = setup.field()
    content_length = env.get('CONTENT_LENGTH', 0)
    try:
        body = env.get('wsgi.input').read(int(content_length))
        data_str_up = urllib.parse.unquote(body.decode())
        data_str = data_str_up.replace('text=','')
        de = json.JSONDecoder()
        data_json = de.decode(data_str)
        rc = t_d.redis_con()
        t_d.insert_receive(SCRfield=SCRfield, rc=rc, receive=data_json)
    except:
        print('error')

    status = '200 OK'
    headers = [('Content-Type', 'text/json; charset=utf-8')]
    return status, headers, [bytes("okok", encoding='utf-8')]




#/static/js/exampl.js
def static(env):
    env_path = env['PATH_INFO']
    ex = env_path.split('.')[-1]

    ex_dic = {
        'js': 'text/javascript',
        'css': 'text/css',
        'html': 'text/html',
        'svg': 'image/svg+xml'
    }

    if(os.path.exists('wsgi' + env_path)):
        status = '200 OK'
        with open('wsgi' + env_path) as f:
            text = f.read()
        headers = [('Content-Type', ex_dic[ex] + '; charset=utf-8')]
    else:
        status = '404 Not Found'
        text = '404 Not Found'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
    
    return status, headers, [t.encode("utf-8") for t in text.split('\n')]

def api_400(env):
    message = '400 Bad Request'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    return message, headers, [message.encode("utf-8")]

def api_404(env):
    message = '404 Not Found'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    return message, headers, [message.encode("utf-8")]

def routing(env):

    router = {
        'GET':{
            '/': api_index,
            '/rest/': api_rest,
            '/static/': static
        },
        'POST':{
            '/': api_index,
            '/receive/': api_receive
        }
    }

    env_method = env['REQUEST_METHOD']
    env_path = env['PATH_INFO']
    if(env['PATH_INFO'] == '/'):
        env_path = '/'
    else:
        env_path = '/' + env_path.split('/')[1] + '/'
    #print(env_path)
        
    if(env_method not in set(['GET', 'POST'])):
        return api_400(env)
    elif(env_path in router[env_method]):
        return router[env_method].get(env_path)(env)
    else:
        return api_404(env)

def app(env, res):
    status, headers, html = routing(env)
    res(status, headers)
    return html



CONF.SCR['module'] = 'WSGI'
slog = S_logger(SCRenv=CONF.SCR)
try:
    httpd = simple_server.make_server(CONF.GUI['address'], CONF.GUI['wsgi_port'], app)
    slog.output(lv='INFO', log='Serving wsgi-gui server on ' + CONF.GUI['address'] + ':' + str(CONF.GUI['wsgi_port']) + '...')
    httpd.serve_forever()
except OSError:
    slog.output(lv='WARN', log='can\'t serve wsgi-gui server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['wsgi_port']) + ' already in use')
except KeyboardInterrupt:
    slog.output(lv='INFO', log='close wsgi server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['web_socket_port']))

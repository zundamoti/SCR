#!/usr/bin/env python3
# coding: utf-8

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
    g_c = Controller()
    html = g_c.get_index()
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    return '200 OK', headers, html

def api_rest(env):
    g_c = Controller()
    json = g_c.get_json(path=env['PATH_INFO'])
    headers = [('Content-Type', 'text/json; charset=utf-8')]
    return '200 OK', headers, [bytes(json, encoding='utf-8')]

def api_receive(env):
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

    headers = [('Content-Type', 'text/json; charset=utf-8')]
    return '200 OK', headers, [bytes("okok", encoding='utf-8')]

def static(env):
    env_path = env['PATH_INFO']
    if(os.path.exists('wsgi' + env_path)):
        with open('wsgi' + env_path) as f:
            text = f.read()
        headers = [content_type_map(env_path)]
    else:
        return api_400(env=env)
    
    return '200 OK', headers, [t.encode("utf-8") for t in text.split('\n')]

def code_static(env):
    env_path = env['PATH_INFO']
    folder = env_path.split('/')[2]
    file_path = '/'.join(env_path.split('/')[4:])
    try:
        with open('code/' + folder + '/static/' + file_path) as f:
            text = f.read()
        headers = [content_type_map(env_path)]
    except Exception as e:
        print(e)
        return api_400(env=env)

    return '200 OK', headers, [t.encode("utf-8") for t in text.split('\n')]

def content_type_map(env_path):
    ex = env_path.split('.')[-1]
    ex_dic = {
        'js': 'text/javascript',
        'css': 'text/css',
        'html': 'text/html',
        'svg': 'image/svg+xml'
    }
    return ('Content-Type', ex_dic[ex] + '; charset=utf-8')


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
        
    if(env_method not in set(['GET', 'POST'])):
        return api_400(env=env)
    elif('code' in env_path):
        return code_static(env=env)
    elif('rest' in env_path):
        return api_rest(env=env)
    elif(env_path in router[env_method]):
        return router[env_method].get(env_path)(env=env)
    else:
        return api_404(env=env)

def gui(env, res):
    status, headers, html = routing(env=env)
    res(status, headers)
    return html


CONF.SCR['module'] = 'WSGI'
slog = S_logger(SCRenv=CONF.SCR)
try:
    httpd = simple_server.make_server(CONF.GUI['address'], CONF.GUI['wsgi_port'], gui)
    slog.output(lv='INFO', log='Serving wsgi-gui server on ' + CONF.GUI['address'] + ':' + str(CONF.GUI['wsgi_port']) + '...')
    httpd.serve_forever()
except OSError:
    slog.output(lv='WARN', log='can\'t serve wsgi-gui server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['wsgi_port']) + ' already in use')
except KeyboardInterrupt:
    slog.output(lv='INFO', log='close wsgi server ' + CONF.GUI['address'] + ':' + str(CONF.GUI['web_socket_port']))

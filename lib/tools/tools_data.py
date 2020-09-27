# coding: utf-8

import os
import glob
import time
import json
from copy import copy

import redis

from lib.tools.s_logger import S_logger
import config as CONF

class Tools_data:

    # pool
    def redis_pool(self, SCRenv):
        try:
            pool = redis.ConnectionPool(
                host=CONF.REDIS['address'],
                port=CONF.REDIS['port'],
                db=CONF.REDIS['db'], 
                decode_responses=True)
            rp = redis.StrictRedis(connection_pool=pool)
            rp.keys()
        except:
            #SCRenv['log'].output("Boot to journal mode.", level='DEBUG', SCRenv={'module':'SCR'})
            return 'journal'
        #SCRenv['log'].output("Boot to redis mode.", level='DEBUG', SCRenv={'module':'SCR'})
        return pool

    def redis_con(self):
        r = redis.StrictRedis(
            host=CONF.REDIS['address'],
            port=CONF.REDIS['port'],
            db=CONF.REDIS['db'],
            decode_responses=True)
        return r


    # serch and get data
    # return <jsonstr>
    def get_data(self, SCRfield, SCRenv, ty):
        
        # field data is only journal
        if ty == 'fi':
            if(os.path.exists('journal/scr_f')):
                with open('journal/scr_f') as f:
                    data_str = f.read()
            else:
                return False
        else:
            key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), ty])
            if type(SCRenv['pool']) == redis.connection.ConnectionPool:
                re = redis.StrictRedis(connection_pool=SCRenv['pool'])
                if(re.exists(key)):
                    if(ty == 'sp'):
                        return re.smembers(key)
                    else:
                        data_str = re.get(key)

                else:
                    if(ty == 'sp'):
                        return set([])
                    return []
            if SCRenv['pool'] == 'journal':
                if(os.path.exists('journal/' + key)):
                    with open('journal/' + key) as f:
                        data_str = f.read()
                else:
                    return False
        #print(data_str)
        de = json.JSONDecoder()
        return de.decode(data_str.replace('\'','\"'))

        
    def pop_receive_data(self, SCRfield, SCRenv):
        data_list = []
        if type(SCRenv['pool']) == redis.connection.ConnectionPool:
            key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), 're'])
            try:
                re = redis.StrictRedis(connection_pool=SCRenv['pool'])
                if(0 < re.llen(key)):
                    low = re.llen(key)
                    data_list += re.lrange(key, 0, low - 1)
                    re.ltrim(key, low, -1)
            except:
                #SCRenv['log'].output("failed receive.", level='DEBUG', SCRenv=SCRenv)
                return False
    
        re_files = glob.glob('journal/*_re_*')
        if(len(re_files) != 0):
            try:
                for ref in re_files:
                    with open(ref) as f:
                        data_str = f.read()
                        data_list += data_str.split('\n')
                    os.remove(ref)
            except:
                #SCRenv['log'].output("failed receive from journal.", level='DEBUG', SCRenv=SCRenv)
                return False

        if(len(data_list) == 0):
            return False
        de = json.JSONDecoder()
        data_dic_list = []
        for re in data_list:
            data_dic_list.append(de.decode(re.replace('\'','\"')))
        return data_dic_list



    # 指定されたデータを作成する
    # return <bool>
    def create_data(self, SCRfield, SCRenv, data, ty):
        if ty == 'fi':
            with open('journal/scr_f', 'w') as f:
                f.write(json.dumps(data))
            return True
        else:
            key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), ty])
            c_data = copy(data)
            if(ty == 'en'):
                del c_data['pool']
                del c_data['i']
                del c_data['log']
                if(type(SCRenv['pool']) == redis.connection.ConnectionPool):
                    c_data['pool'] = 'redis_pool'
                else:
                    c_data['pool'] = 'journal'
                    
        if type(SCRenv['pool']) == redis.connection.ConnectionPool:
            try:
                re = redis.StrictRedis(connection_pool=SCRenv['pool'])
                re.set(key, json.dumps(c_data))
            except:
                SCRenv['log'].output(lv='DEBUG', log="failed set " + key + " data.")
                return False
        elif SCRenv['pool'] == 'journal':
            try:
                if(os.path.exists('journal/' + key)):
                    os.remove('journal/' + key)
                with open('journal/' + key, 'w') as f:
                    f.write(json.dumps(c_data))
            except:
                #SCRenv['log'].output("failed write " + key + " journal data.", level='DEBUG', SCRenv=SCRenv)
                return False
        return True
    
    # 指定されたデータを消去する
    # return <bool>
    def truncate_data(self, SCRfield, SCRenv, ty):
        
        key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), ty])
        if type(SCRenv['pool']) == redis.connection.ConnectionPool:
            try:
                re = redis.StrictRedis(connection_pool=SCRenv['pool'])
                re.delete(key)
            except:
                #SCRenv['log'].output("failed truncate " + key + ".", level='DEBUG', SCRenv=SCRenv)
                return False
        elif SCRenv['pool'] == 'journal':
            try:
                os.remove('journal/' + key)
            except:
                #SCRenv['log'].output("failed truncate " + key + ".", level='DEBUG', SCRenv=SCRenv)
                return False
        return True


    def insert_spe(self, SCRfield, SCRenv, data):
        key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), 'sp'])
        if type(SCRenv['pool']) == redis.connection.ConnectionPool:
            try:
                re = redis.StrictRedis(connection_pool=SCRenv['pool'])
                return re.sadd(key, data)
            except:
                #SCRenv['log'].output("failed truncate " + key + ".", level='DEBUG', SCRenv=SCRenv)
                return False

        
    def insert_receive(self, SCRfield, rc, receive):
        key = '_'.join(['scr', str(SCRfield['state']['fid']), str(SCRfield['state']['myid']), 're'])
        rc.rpush(key, json.dumps(receive))
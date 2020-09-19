# coding: utf-8

from lib.setup import Setup

from lib.tools.tools_data import Tools_data
from lib.tools.s_logger import S_logger
import config as CONF

class Controller:
    
    def get_json(self, path):
        t_d = Tools_data()
        setup = Setup()
        SCRfield = setup.field()
        
        if('/get_scr/' in path):
            ty = path.split('/')[-2]
            key = '_'.join([
                'scr',
                str(SCRfield['state']['fid']),
                str(SCRfield['state']['myid']),
                ty])
        elif('/get_data/' in path):
            key = path.split('/')[-2]
            
        rc = t_d.redis_con()
        return rc.get(key)


    def websocket_chaser(self, SCRfield, GUIenv, GUIraw):
        t_d = Tools_data()
        send_json = {}

        if(not GUIraw['field']):
            send_json["field"] = SCRfield
            GUIraw['field'] = True

        SCRschedule = t_d.get_data(
            SCRfield=SCRfield, SCRenv=GUIenv, ty='sc')
        if(GUIraw['schedule'] != str(SCRschedule)):
            GUIraw['schedule'] = str(SCRschedule)
            send_json['schedule'] = SCRschedule

        SCRenv = t_d.get_data(
            SCRfield=SCRfield, SCRenv=GUIenv, ty='en')
        if(GUIraw['env'] != str(SCRenv)):
            GUIraw['env'] = str(SCRenv)
            send_json['env'] = SCRenv

        SCRcodes = t_d.get_data(
            SCRfield=SCRfield, SCRenv=GUIenv, ty='co')
        if(GUIraw['codes'] != str(SCRcodes)):
            GUIraw['codes'] = str(SCRcodes)
            send_json['codes'] = SCRcodes
        
        return send_json, GUIraw
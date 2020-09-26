# coding: utf-8

from lib.setup import Setup

from lib.tools.tools_data import Tools_data
from lib.tools.tools_file import Tools_file
from lib.tools.s_logger import S_logger
import config as CONF

class Controller:
    
    def get_json(self, path):
        t_d = Tools_data()
        
        if('/get_redis/' in path):
            key = path.split('/')[3]
            
        rc = t_d.redis_con()
        return rc.get(key)

    def get_index(self):
        t_f = Tools_file()
        SCRcodes = t_f.get_codes()
        switch_html, include_html, add_script, add_view = t_f.get_codes_html(SCRcodes=SCRcodes)
        with open('wsgi/index.html') as f:
            index_html = f.read()
        text_list = [t.encode("utf-8") for t in index_html.split('\n')]
        html = []
        for tli in range(len(text_list)):
            low_text = text_list[tli].decode('utf-8')
            if("@code_html_switch" in low_text):
                html = html + switch_html.split('\n')
            elif("@code_html_include" in low_text):
                html = html + include_html.split('\n')
            elif("@code_js_add" in low_text):
                html = html + add_script.split('\n')
            elif("@code_view_add" in low_text):
                html = html + add_view.split('\n')
            else:
                html.append(text_list[tli])
        n = bytes('\n', encoding='utf-8')
        return [ bytes(t, encoding='utf-8') + n if type(t) == str else t + n for t in html ]


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
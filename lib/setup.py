# coding: utf-8

from lib.tools.tools_data import Tools_data
from lib.tools.tools_process import Tools_process
from lib.tools.tools_system import Tools_system
from lib.tools.tools_time import Tools_time
from lib.tools.s_logger import S_logger

import config as CONF

class Setup:

    def field(self):
        t_d = Tools_data()

        SCRfield = t_d.get_data(
            SCRfield=False, SCRenv=False, ty='fi')
        # fieldジャーナルの存在をチェック
        if SCRfield:
            return SCRfield
        else:
            # 存在しない場合は新規作成かchain-create
            tempSCRfield = CONF.DEFAULT_FIELD
            #if arg_obj.chain: # chain-createは引数が渡される
                # chain createで作る(scrctl chain-create 経由の起動のみ)
                 # 渡されているファイルを見て自分のfidを調べ新しくidを振る
                #tempSCRfield.state.fid, tempSCRfield.state.envid = to.get_other_id()
            # 書き込み
            if not t_d.create_data(
                SCRfield=False, SCRenv=False, ty='fi', data=tempSCRfield):
                pass
                # 作る事がで.warning('')
            return tempSCRfield

    def env(self, SCRfield, roll):
        t_s = Tools_system()
        t_t = Tools_time()
        t_d = Tools_data()
        t_p = Tools_process()
        SCRenv = CONF.SCR
        SCRenv['befor'] = t_t.now_sec()
        SCRenv['now'] = t_t.now_sec()
        SCRenv['module'] = roll
        SCRenv = t_s.get_env(SCRenv=SCRenv)
        SCRenv['i'] = {}
        SCRenv['log'] = S_logger(SCRenv=SCRenv)

        if(roll == 'SCR'):
            SCRenv = t_p.run_server(SCRenv=SCRenv)
            SCRenv['sub_state'] = []
            for i in range(SCRenv['max_sub_process']):
                SCRenv['sub_state'].append({i:0})

        if(roll in ('SCR', 'SUB', 'WS')):
            SCRenv['pool'] = t_d.redis_pool(SCRenv=SCRenv)
        else:
            SCRenv['pool'] = 'ins_redis'
        return SCRenv

    def tasks(self, SCRfield, SCRenv):
        t_d = Tools_data()
        SCRtasks = t_d.get_data(
            SCRenv=SCRenv, SCRfield=SCRfield, ty='ta')
        if SCRtasks == False:
            return []
        return SCRtasks

    def shut_down(self, SCRenv):
        if(SCRenv['gui']):
            t_p = Tools_process()
            t_p.kill_process(pid=SCRenv['http_server_pid'])
            t_p.kill_process(pid=SCRenv['websocket_server_pid'])
        exit(0)
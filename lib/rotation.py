# coding: utf-8

from lib.tools.tools_data import Tools_data
from lib.tools.tools_process import Tools_process
from lib.tools.tools_time import Tools_time
from lib.tools.s_logger import S_logger

class Rotation:

    # タスクの状況管理とサブプロセスの立ち上げ
    def task_run(self, SCRfield, SCRenv, SCRtasks):
        t_t = Tools_time()
        t_p = Tools_process()
        t_d = Tools_data()

        # get now second
        t_t.sleep(SCRenv['pulse_rate'])
        SCRenv['now'] = t_t.now_sec()
        
        # if haven't task then maxtid be 0 
        if 0 == len(SCRtasks):
            SCRenv['max_tid'] = 0
            t_d.truncate_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sp')
            return SCRenv, SCRtasks

        ## task manegiment

        # 未割り当てタスクにsubidを割り当てる
        # 並行して残すtaskのみをtempSCRtasksに追加する
        tempSCRtasks = []
        SCRspe = t_d.get_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sp')
        if(False == SCRspe):
            SCRspe = []
        for task in SCRtasks:
            if task['sub_id'] == -1:
                # 未割り当てであれば
                task['sub_id'] = t_p.empty_sub(
                    SCRenv=SCRenv, SCRtasks=SCRtasks, tempSCRtasks=tempSCRtasks)
                tempSCRtasks.append(task)
            elif str(task['tid']) not in SCRspe:
                tempSCRtasks.append(task)
        if 0 == len(tempSCRtasks):
            return SCRenv, tempSCRtasks
        
        ## FlaskとSubへの共有用タスクデータを反映させる
        #t_d.truncate_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='sp')
        t_d.create_data(SCRfield=SCRfield, SCRenv=SCRenv, ty='ta', data=tempSCRtasks)


        ## sub立ち上げ

        # 子プロセスの状態チェック開始
        running_sub, exclude = t_p.get_child_pid(SCRenv=SCRenv)
        # 子プロセスがmax使用なら中断
        if SCRenv['max_sub_process'] <= len(running_sub) - exclude:
            return SCRenv, tempSCRtasks
        # 立ち上げる必要のあるsub_idを探す
        start_sub = t_p.need_wake_sub(SCRenv=SCRenv, SCRtasks=tempSCRtasks, running_sub=running_sub)
        # 立ち上げる
        SCRenv = t_p.start_sub(SCRenv=SCRenv, start_sub=start_sub)

        return SCRenv, tempSCRtasks

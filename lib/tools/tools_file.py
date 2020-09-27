# coding: utf-8

import os
from glob import glob

class Tools_file:

    def get_codes(self):
        SCRcords = []
        path_list_1 = glob('code/*')
        for path_1 in path_list_1:
            folder_name = path_1[5:]
            if folder_name == 'ignore':
                continue
            file_list = []
            path_list_2 = glob('code/' + folder_name + '/*')
            for path_2 in path_list_2:
                file_name = path_2[6+len(folder_name):]
                file_list.append(file_name)
            SCRcords.append( { "folder_name":folder_name, "file_list":file_list } )
        return SCRcords
    

    def get_codes_html(self, SCRcodes):
        switch_html = ''
        include_html = ''
        add_script = ''
        add_view = ''
        for code in SCRcodes:
            if(os.path.exists('code/' + code['folder_name'] + '/static/code.html')):
                include_html = include_html + '<div v-if=disp.code_' + code['folder_name'] + ' class="main-area">\n'
                with open('code/' + code['folder_name'] + '/static/code.html') as f:
                    include_html = include_html + f.read()
                include_html = include_html + '</div>\n'
                switch_html = switch_html + '<div v-on:click="$_disp_change(\''
                switch_html = switch_html + 'code_' + code['folder_name']
                switch_html = switch_html + '\')" class="schedule-task icon-box">\n<div class="icon"><object data="/code/'
                switch_html = switch_html + code['folder_name']
                switch_html = switch_html + '/static/icon.svg" type="image/svg+xml" width="24" height="24"></object></div>\n</div>\n'
                add_script = add_script + '<script src="/code/' + code['folder_name'] + '/static/code.js"></script>\n'
                add_view = add_view + 'temp_scr.data.disp.code_' + code['folder_name'] + ' = false;\n'
        return switch_html, include_html, add_script, add_view


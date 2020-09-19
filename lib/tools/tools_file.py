# coding: utf-8

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
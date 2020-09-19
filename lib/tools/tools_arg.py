# coding: utf-8

import json

import argparse

import config as CONF



class Tools_arg:

    def args_get(self):
        return argparse.ArgumentParser(description='scr control command')
        
    def parser_args(self, parser):
        parser.add_argument('-sec', default=0, type=int)
        parser.add_argument('--days1', default=0, action='store_true')
        parser.add_argument('-path', required=True, type=str)
        parser.add_argument('-c', default="")
        parser.add_argument('-data_key', default=0)
        parser.add_argument('-priority', default="")
        return parser.parse_args()


    def args_to_re(self, args):
        newSCRreceive = CONF.DEFAULT_RECEIVE
        if('sec' in args):
            newSCRreceive['sec'] = args.sec
        if(args.days1):
            newSCRreceive['days1'] = True
        else:
            newSCRreceive['days1'] = False
        newSCRreceive['c'] = args.c
        newSCRreceive['d'] = CONF.DEFAULT_DETAILS
        newSCRreceive['d']['priority'] = args.priority
        newSCRreceive['d']['lang'] = CONF.SCRCTL['code_exec'][args.path.split('.')[-1]]
        newSCRreceive['d']['data_key'] = args.data_key
        newSCRreceive['d']['file_path'] = args.path.split('/')[0]
        newSCRreceive['d']['file_name'] = args.path.split('/')[1]
        return newSCRreceive
        


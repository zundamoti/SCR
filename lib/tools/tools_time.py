# coding: utf-8

import time
from datetime import datetime

class Tools_time():
    def now_sec(self):
        now = datetime.now()
        now_m = int(now.strftime('%M'))
        now_h = int(now.strftime('%H'))
        now_s = int(now.strftime('%S'))
        return now_s + ( now_m + now_h * 60 ) * 60
    
    def sleep(self, howlong):
        time.sleep(howlong)
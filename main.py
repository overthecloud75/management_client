import os
import threading
import time
from logging.config import dictConfig
from datetime import datetime

from utils.analyze import Analyze
from utils.log import send_log_list
from configs import BASE_DIR, LOG_DIR, WEB_SERVER_TYPE

def read_log():

    analyze = Analyze(interval=10000)  
    while True:
        # timestamp를 refresh
        analyze.timestamp = datetime.now()
        
        if WEB_SERVER_TYPE == 'nginx':
            access_log_list = analyze.read_nginx_access_log()
        elif WEB_SERVER_TYPE == 'iis':
            access_log_list = analyze.read_iis_access_log()

        status = False 
        if access_log_list:
            status = send_log_list(access_log_list)

        if status:
            analyze.previous_timestamp = analyze.timestamp

        time.sleep(300)

if __name__ == '__main__':
    read_log()

import os

# log
BASE_DIR= os.getcwd()
LOG_DIR = 'logs'

if os.path.exists(os.path.join(BASE_DIR, LOG_DIR)):
    pass
else:
    os.mkdir(os.path.join(BASE_DIR, LOG_DIR))

ACCESS_LOG_DIR = 'web_logs'

MANAGEMENT_TYPE = 'client'
WEB_SERVER_TYPE = 'iis'
LOCAL_HOURS = 9 

ACCESS_LOG_KEYS = ['timestamp', 'ip', 'host', 'method', 'url', 'http_version', 'status', 'size', 'referer', 'user_agent', 'body', 'request_time', 'geo_ip']
AUTH_LOG_KEYS = ['timestamp', 'client', 'ip', 'id', 's_port', 'geo_ip']

AUTH_LOG_FILTERING = ['Invalid user', 'invalid user', 'Disconnected from authenticating user', 'Failed password for', 'from', 
            'Connection closed by invalid user', 'Disconnected', 'port', 'Connection closed by authenticating user', 'Failed none for', 
            'Accepted publickey for ']


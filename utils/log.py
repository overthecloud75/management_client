import requests

from configs import FIREWALL_SITE

def send_log_list(log_list):
    url = FIREWALL_SITE + 'api/remote/log'
    status = False
    try:
        res = requests.post(url, json=log_list, timeout=3)
        if res.status_code == 200:
            status = True 
    except Exception as e:
        print(e)
    return status 
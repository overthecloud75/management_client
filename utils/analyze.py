from datetime import datetime, timedelta
import os
import re 
import csv
import logging

from configs import ACCESS_LOG_DIR, LOCAL_HOURS, MANAGEMENT_TYPE
    
class Analyze:

    def __init__(self, interval=10, unit='m'):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Analyze Start')

        if unit == 'm':
            self.interval = interval * 60
        else:
            self.interval = interval

        self.timestamp = datetime.now()
        print(self.timestamp)
        self.previous_timestamp  = self.timestamp - timedelta(seconds=self.interval)

    def _parse_nginx_access_log(self, line):

        # https://pythonmana.com/2021/04/20210417005158969I.html
        LOG_REGEX = re.compile(r'(?P<ip>.*?)- - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)" (?P<rt>.*?) "(?P<host>.*?)" "(?P<body>.*?)" (?P<scheme>.*?) ')
        result = LOG_REGEX.match(line)

        ip = result.group('ip')[:-1]
        datetime_timestamp = datetime.strptime(result.group('time')[:-6], '%d/%b/%Y:%H:%M:%S')

        request = result.group('request')
        request_list = request.split(' ')
        if len(request_list) == 3:
            method = request_list[0]
            url = request_list[1]
            http_version = request_list[2]
        else:
            method = '-'
            url = request
            http_version = '-'
        status = int(result.group('status'))
        size = int(result.group('bytes'))
        referer = result.group('referer')
        user_agent = result.group('ua')
        request_time = result.group('rt')
        host = result.group('host')
        if host == '':
            host = '-'
        body = result.group('body')
        scheme = result.group('scheme')

        log_dict = {'timestamp': datetime_timestamp, 'ip': ip, 'host': host, 'method': method, 'scheme': scheme, 'url': url, 
                'http_version': http_version, 'status': status, 'size': size, 'referer': referer, 'user_agent': user_agent, 'body': body, 'request_time': request_time}

        return log_dict

    def _parse_iis_access_log(self, line):

        line = line.replace('\n', '')
        line_list = line.split(' ')

        timestamp = line_list[0] + ':' + line_list[1]
        datetime_timestamp = ''
        try:
            datetime_timestamp = datetime.strptime(timestamp, '%Y-%m-%d:%H:%M:%S')
        except Exception as e:
            log_dict = {}
        else:
            datetime_timestamp = datetime_timestamp + timedelta(hours=9)
            url_list = line_list[11].split(':')
            scheme = url_list[0]
            log_dict = {'ip': line_list[2], 'host': line_list[12], 'method': line_list[3], 'scheme': scheme, 'url': line_list[4], 
                    'http_version': line_list[9], 'status': line_list[13], 'size': '-', 'referer': '-', 'user_agent': line_list[10], 'body': '-', 'request_time': '-'}

            if MANAGEMENT_TYPE == 'client':
                log_dict['timestamp'] = datetime_timestamp.strftime('%Y-%m-%d:%H:%M:%S')
            else:
                log_dict['timestamp'] = datetime_timestamp

        return datetime_timestamp, log_dict

    def read_nginx_access_log(self):

        log_list = []
        with open(NGINX_ACCESS_LOG_PATH, 'r', encoding='utf-8') as f:
            reverse_lines = f.readlines()[::-1]
            for line in reverse_lines:
                try:
                    log_dict = self._parse_nginx_access_log(line)
                    if log_dict['timestamp'] < self.previous_timestamp:
                        break
                    log_list.append(log_dict)
                except Exception as e:
                    self.logger.error('{}: {}'.format(e, line))
        return log_list
    
    def read_iis_access_log(self):

        log_list = []
        dir_list = os.listdir(ACCESS_LOG_DIR)
        ACCESS_LOG_PATH = os.path.join(ACCESS_LOG_DIR, dir_list[-1])
        with open(ACCESS_LOG_PATH, 'r', encoding='utf-8') as f:
            reverse_lines = f.readlines()[::-1]
            for line in reverse_lines:
                datetime_timestamp, log_dict = self._parse_iis_access_log(line)
                if log_dict:
                    if datetime_timestamp < self.previous_timestamp:
                        break
                    log_list.append(log_dict)
        return log_list

if __name__ == '__main__':
    analyze = Analyze()
    # nginx_log_list = analyze.read_nginx_access_log()
    auth_log_list = analyze.read_auth_log()
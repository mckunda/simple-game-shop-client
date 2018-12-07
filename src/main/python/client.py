import re
import sys
import socket
import configparser

from helpers.json_message import json_recv, json_send

cfg = configparser.ConfigParser()

cfg.read('config.ini')


class GameShopClient:
    def __init__(self):
        self.uid = None
        self.host = cfg['client']['host']
        self.port = int(cfg['client']['port'])
        self.soc = None
        self.session_active = False

    def __connect(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.soc.connect((self.host, self.port))
        except:
            print("Connection error")
            sys.exit()

        self.session_active = True

    def __disconnect(self):
        self.uid = None
        self.soc.close()
        self.soc = None
        self.session_active = False

    @staticmethod
    def __preprocess_query(query_s, uid):
        query = re.sub(' +', ' ', query_s).split()
        if len(query) < 2:
            query.append(None)
        return {'action': query[0].upper(), 'params': query[1], 'user_id': uid}

    def __process_response(self, res, login=False):
        if 'status' in res:
            if res['status'] == 'OK':
                if login:
                    self.uid = res['user_id']
                if res['message']:
                    print(res['message'])
                if res['data']:
                    self.__print_response(res['data'])
            elif res['status'] == 'ERR':
                if 'message' in res:
                    print('ERROR: ' + res['message'])
                else:
                    print('UNKNOWN ERROR')
            elif res['status'] == 'LOGOUT':
                self.__disconnect()
            else:
                print('UNKNOWN ERROR')
        else:
            print('UNKNOWN ERROR')

    def __print_response(self, res):
        self.__print_table(res)

    @staticmethod
    def __print_table(data, col_list=None):
        """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
        If column names (colList) aren't specified, they will show in random order.
        Author: Thierry Husson - Use it as you want but don't blame me.
        """
        if not col_list:
            col_list = list(data[0].keys() if data else [])
        my_list = [col_list]  # 1st row = header
        for item in data:
            my_list.append([str(item[col] or '') for col in col_list])
        col_size = [max(map(len, col)) for col in zip(*my_list)]
        format_str = ' | '.join(["{{:<{}}}".format(i) for i in col_size])
        my_list.insert(1, ['-' * i for i in col_size])  # Separating line
        for item in my_list:
            print(format_str.format(*item))

    def __print_help(self):
        if self.session_active:
            print(cfg['help']['logged in'])
        else:
            print(cfg['help']['anonymous'])

    def __del__(self):
        if self.session_active and self.uid is not None:
            json_send(self.soc, {'action': 'LOGOUT'})
            self.__disconnect()

    def query(self, query_s):
        query_s = query_s.strip()
        if not query_s:
            print('Please enter a valid query.')
            return

        if query_s == 'HELP':
            self.__print_help()
            return

        query = self.__preprocess_query(query_s, self.uid)

        if not self.session_active:
            self.__connect()

        json_send(self.soc, query)

        res = json_recv(self.soc)

        self.__process_response(res, login='LOGIN' in query_s.upper())

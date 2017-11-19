#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Hammer
@license: Apache Licence 
@contact: tianhanming11@gmail.com
@software: PyCharm Community Edition
@file: calculator_5.py
@time: 2017/11/19 下午2:42
"""

import sys, os, getopt, configparser
from multiprocessing import Pool, Queue, Process
from datetime import datetime

TAX_POINT = 3500
TAX_TABLE = [
    (80000, 0.45, 13505),
    (55000, 0.35, 5505),
    (35000, 0.30, 2755),
    (9000, 0.25, 1005),
    (4500, 0.2, 555),
    (1500, 0.1, 105),
    (0, 0.03, 0),
]


class Config(object):
    def __init__(self, path, city):
        self.path = path
        self.city = city
        self._config = {}

    def read_config(self):
        conf = configparser.ConfigParser()
        conf.read(self.path)
        if self.city in conf.sections() or self.city == 'DEFAULT':
            for line in conf.items(self.city):
                self._config[line[0]] = float(line[1])
            return self._config
        else:
            print("Don't have this city's config")
            exit(1)

    def __get_config(self, config_name):
        return self.read_config()[config_name]

    @property
    def get_JiShuL(self):
        return self.__get_config('jishul')

    @property
    def get_JiShuH(self):
        return self.__get_config('jishuh')

    @property
    def get_total_social_safe(self):
        return sum([
            self.__get_config('yanglao'),
            self.__get_config('yiliao'),
            self.__get_config('shiye'),
            self.__get_config('gongshang'),
            self.__get_config('shengyu'),
            self.__get_config('gongjijin')
        ])


class UserData(object):
    def __init__(self, path, opath):
        self.path = path
        self.opath = opath
        self._user_data = []

    def read_user_data(self):
        # print('Run task1 as pid{}'.format(os.getpid()))
        with open(self.path) as file:
            for lines in file:
                line = lines.strip().split(',')
                self._user_data.append(line)
        # return self._user_data
        queue.put(self._user_data)

    def calculator(self):
        # print('Run task2 as pid{}'.format(os.getpid()))
        social_safe = config.get_total_social_safe
        JiShuL = config.get_JiShuL
        JiShuH = config.get_JiShuH
        user_datas = queue.get()
        # print(user_datas)
        user_data_list = []
        for user_data in user_datas:
            job_nu = int(user_data[0])
            salary = int(user_data[1])
            if salary >= JiShuH:
                social_cardinal = JiShuH
            elif salary <= JiShuL:
                social_cardinal = JiShuL
            else:
                social_cardinal = salary

            social_sec = social_cardinal * social_safe
            tax = salary - social_sec
            taxable_in = tax - TAX_POINT
            now = datetime.now()
            now_str = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')

            if tax <= TAX_POINT:
                user_data_list.append('{},{:.2f},{:.2f},0.00,{:.2f},{}\n'.format(job_nu, salary, social_sec, tax, now_str))

            for i in TAX_TABLE:
                if taxable_in > i[0]:
                    taxable_am = taxable_in * i[1] - i[2]
                    tax = tax - taxable_am
                    user_data_list.append(
                        '{},{:.2f},{:.2f},{:.2f},{:.2f},{}\n'.format(job_nu, salary, social_sec, taxable_am, tax, now_str))
                    break
        # return user_data_list
        queue.put(user_data_list)

    def dump_to_file(self):
        # print('Run task3 as pid{}'.format(os.getpid()))
        user_data_lines = queue.get()
        # print(user_data_lines)
        with open(self.opath, 'a') as file:
            for user_data_line in user_data_lines:
                file.write(user_data_line)
        return


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help", "city=", "config=", "data=", "output"])
        for name, opt in opts:
            if name in ('-h', '--help'):
                print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
                exit(0)
            if name in ('-C', '--city'):
                city = opt.upper()
            else:
                city = 'DEFAULT'
            if name in ('-c', '--config'):
                cfg_file_path = opt
            if name in ('-d', '--data'):
                user_file_path = opt
            if name in ('-o', '--output'):
                gongzi_file_path = opt
        # print(city, user_file_path, cfg_file_path, gongzi_file_path)
    except (getopt.GetoptError, NameError):
        print("Parameter Error")
        exit(1)

    if os.path.exists(cfg_file_path) and os.path.exists(user_file_path):
        queue = Queue()
        config = Config(cfg_file_path, city)
        user = UserData(user_file_path, gongzi_file_path)
        p_read_user_info = Process(target=user.read_user_data)
        p_build_user_data = Process(target=user.calculator)
        p_dump_to_file = Process(target=user.dump_to_file)
        p_read_user_info.start()
        p_read_user_info.join()
        p_build_user_data.start()
        p_build_user_data.join()
        p_dump_to_file.start()
        p_dump_to_file.join()
    else:
        print('Path Error: No such file or directory')

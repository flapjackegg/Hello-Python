#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Hammer
@license: Apache Licence 
@contact: tianhanming11@gmail.com
@software: PyCharm Community Edition
@file: calculator_4.py
@time: 2017/11/17 下午4:53
"""

from multiprocessing import Pool, Queue, Process
import sys, os

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
    def __init__(self, path):
        self.path = path
        self._config = {}

    def read_config(self):
        with open(self.path) as file:
            for lines in file:
                line = lines.strip().split(' = ')
                self._config[line[0]] = float(line[1])
        return self._config

    def __get_config(self, config_name):
        return self.read_config()[config_name]

    @property
    def get_JiShuL(self):
        return self.__get_config('JiShuL')

    @property
    def get_JiShuH(self):
        return self.__get_config('JiShuH')

    @property
    def get_total_social_safe(self):
        return sum([
            self.__get_config('YangLao'),
            self.__get_config('YiLiao'),
            self.__get_config('ShiYe'),
            self.__get_config('GongShang'),
            self.__get_config('ShengYu'),
            self.__get_config('GongJiJin')
        ])


class UserData(object):
    def __init__(self, path, opath):
        self.path = path
        self.opath = opath
        self._user_data = []

    def read_user_data(self):
        print('Run task1 as pid{}'.format(os.getpid()))
        with open(self.path) as file:
            for lines in file:
                line = lines.strip().split(',')
                self._user_data.append(line)
        # return self._user_data
        queue.put(self._user_data)

    def calculator(self):
        print('Run task2 as pid{}'.format(os.getpid()))
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

            if tax <= TAX_POINT:
                user_data_list.append('{},{:.2f},{:.2f},0.00,{:.2f}\n'.format(job_nu, salary, social_sec, tax))

            for i in TAX_TABLE:
                if taxable_in > i[0]:
                    taxable_am = taxable_in * i[1] - i[2]
                    tax = tax - taxable_am
                    user_data_list.append(
                        '{},{:.2f},{:.2f},{:.2f},{:.2f}\n'.format(job_nu, salary, social_sec, taxable_am, tax))
                    break
        # return user_data_list
        queue.put(user_data_list)




    def dump_to_file(self):
        # user_data_lines = self.calculator()
        print('Run task3 as pid{}'.format(os.getpid()))
        user_data_lines = queue.get()
        print(user_data_lines)
        with open(self.opath, 'a') as file:
            for user_data_line in user_data_lines:
                file.write(user_data_line)
        return

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        cfg_file_path = args[args.index('-c') + 1]
        user_file_path = args[args.index('-d') + 1]
        gongzi_file_path = args[args.index('-o') + 1]
    except (ValueError, IndexError):
        print('Parameter Error')

    if os.path.exists(cfg_file_path) and os.path.exists(user_file_path):
        queue = Queue()
        config = Config(cfg_file_path)
        user = UserData(user_file_path, gongzi_file_path)
        p_read_user_info = Process(target=user.read_user_data)
        p_build_user_data = Process(target=user.calculator)
        p_dump_to_file = Process(target=user.dump_to_file)
        p_read_user_info.start()
        p_build_user_data.start()
        p_dump_to_file.start()
        p_read_user_info.join()
        p_build_user_data.join()
        p_dump_to_file.join()
        # user.read_user_data()
        # user.calculator()
    else:
        print('Path Error: No such file or directory')
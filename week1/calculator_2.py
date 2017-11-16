#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Hammer
@license: Apache Licence 
@contact: tianhanming11@gmail.com
@software: PyCharm Community Edition
@file: calculator_2.py
@time: 2017/11/15 下午9:28

tax: 税后工资
tax_point: 起征税点
social_sec: 五险一金
taxable_in: 应纳税所得额
taxable_am: 应纳税额
"""

import sys

tax_table = [
    (80000, 0.45, 13505),
    (55000, 0.35, 5505),
    (35000, 0.30, 2755),
    (9000, 0.25, 1005),
    (4500, 0.2, 555),
    (1500, 0.1, 105),
    (0, 0.03, 0),
]


def calculator(job_nu, salary):
    tax_point = 3500
    social_sec = salary * 0.165
    tax = salary - social_sec
    taxable_in = tax - tax_point
    if tax <= tax_point:
        return '{}:{:.2f}'.format(job_nu, tax)

    for i in tax_table:
        if taxable_in > i[0]:
            taxable_am = taxable_in * i[1] - i[2]
            tax = tax - taxable_am
            return '{}:{:.2f}'.format(job_nu, tax)


if __name__ == '__main__':
    for para in sys.argv[1:]:
        income_info = para.split(':')
        try:
            income = int(income_info[1])
            job_nu = int(income_info[0])
        except ValueError:
            print("Parameter Error")
            continue

        print(calculator(job_nu, income))

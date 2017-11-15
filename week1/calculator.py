#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Hammer
@license: Apache Licence 
@contact: tianhanming11@gmail.com
@software: PyCharm Community Edition
@file: calculator.py
@time: 2017/11/15 下午4:19
"""
import sys


def calculator(salary):
    tax_point = 3500
    social_sec = 0
    tax = 0
    if salary <= tax_point:
        print(tax)

    taxable = salary - social_sec - tax_point

    # print(taxable)
    if taxable > 0 and taxable <= 1500:
        tax = taxable * 0.03 - 0
        print(tax)

    if taxable > 1500 and taxable <= 4500:
        tax = taxable * 0.1 - 105
        print(tax)

    if taxable > 4500 and taxable <= 9000:
        tax = taxable * 0.2 - 555
        print(tax)

    if taxable > 9000 and taxable <= 35000:
        tax = taxable * 0.25 - 1005
        print(tax)

    if taxable > 35000 and taxable <= 55000:
        tax = taxable * 0.3 - 2755
        print(tax)

    if taxable > 55000 and taxable <= 80000:
        tax = taxable * 0.35 - 5505
        print(tax)

    if taxable > 80000:
        tax = taxable * 0.45 - 13505
        print(tax)


if __name__ == '__main__':
    salary = sys.argv[1].strip()
    if salary.isdigit():
        calculator(int(salary))
    else:
        print("Parameter Error")

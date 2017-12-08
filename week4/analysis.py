#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd


def analysis(file, user_id):
    try:
        data_json = pd.read_json(file)
    except ValueError:
        return 0,0
    try:
        user_data = data_json[data_json['user_id'] == user_id]['minutes']
    except KeyError:
        return 0
    return user_data.count(), user_data.sum()


def main():
    if len(sys.argv) != 3:
        exit(-1)
    try:
        file = sys.argv[1]
        user_id = int(sys.argv[2])
    except (ValueError, TypeError):
        return 0
    print(analysis(file, user_id))


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def analysis(file, user_id):
    try:
        data_json = pd.read_json(file)
    except ValueError:
        return 0
    try:
        user_id = int(user_id)
        user_data = data_json[data_json['user_id'] == user_id]['minutes']
    except (KeyError, TypeError):
        return 0
    return user_data.count(), user_data.sum()


print(analysis('user_study.json', '1'))

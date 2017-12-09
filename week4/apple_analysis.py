#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def quarter_volume():
    try:
        data = pd.read_csv('apple.csv', header=0)
    except ValueError:
        return 0, 0
    newdata = data.Volume
    newdata.index = pd.to_datetime(data.Date)
    season_volume = newdata.resample('Q').sum()
    second_volume = season_volume.sort_values()[-2]
    return second_volume


if __name__ == '__main__':
    print(quarter_volume())

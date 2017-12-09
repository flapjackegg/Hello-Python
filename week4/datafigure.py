#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def analysis():
    try:
        data_json = pd.read_json('user_study.json')
    except ValueError:
        return 0, 0
    user_data = data_json[['user_id', 'minutes']].groupby('user_id').sum()
    top_100 = user_data[:100]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    ax.plot(top_100.index, top_100.minutes)
    plt.show()


if __name__ == '__main__':
    analysis()

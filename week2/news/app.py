#!/usr/bin/env python3
# encoding: utf-8

"""
@author: Hammer
@license: Apache Licence 
@contact: tianhanming11@gmail.com
@software: PyCharm Community Edition
@file: app.py
@time: 2017/11/22 下午5:23
"""

import os, json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Files(object):
    def __init__(self):
        self.path = os.listdir('../files/')

    def read_json(self):
        dict_list = {}
        for filename in self.path:
            file_path = os.path.join('../files', filename)
            # return self.path
            with open(file_path) as file:
                dicts = json.loads(file.read())
                dict_list[filename] = dicts
        return dict_list

    def get_title(self):
        title_list = []
        for i in self.read_json().values():
            title_list.append(i['title'])
        return title_list

    def get_json_info(self, filename):
        return self.read_json()[filename + '.json']

files = Files()

@app.route('/')
def index():
    titles = files.get_title()
    return render_template('index.html', titles = titles)

@app.route('/files/<filename>')
def file(filename):
    try:
        json_info = files.get_json_info(filename)
    except KeyError:
        abort(404)

    return render_template('file.html', info = json_info)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

def filter(str):
    filter_str = str.replace('\\\\n', '')
    filter_str = filter_str.replace('\\n', '')
    return filter_str

app.add_template_filter(filter)


if __name__ == '__main__':
    app.run(port = 3000)
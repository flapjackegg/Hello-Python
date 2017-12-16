# encoding: utf-8

import os
import json
from flask import Flask


def create_app():
    app = Flask('rmon')
    cfg_file = os.environ.get('RMON_CONFIG')
    cfg = ''
    try:
        with open(cfg_file) as f:
            for line in f:
                line = line.strip()
                if '#' in line:
                    continue
                cfg += line
    except FileNotFoundError:
        print('No such file or directory')
        return app
    
    dict_cfg = json.loads(cfg)
    for key, value in dict_cfg.items():
        app.config[key] = value
    return app

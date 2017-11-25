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

from datetime import datetime
from flask import Flask, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hammer@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)


class File(db.Model):
    # __tablename__ = 'file'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref = db.backref('file', lazy='dynamic'))

    def __init__(self, title, category, content, created_time=None):
        self.title = title
        self.content = content
        self.category = category
        if created_time is None:
            self.created_time = datetime.utcnow()

    def __repr__(self):
        return "<File(title %r)>" % self.title

class Category(db.Model):
    # __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r)>' % self.name


@app.route('/')
def index():
    post_info = File.query.all()
    return render_template('index.html', post_info = post_info)

@app.route('/files/<file_id>')
def file(file_id):
    post = File.query.filter_by(id = file_id).first_or_404()
    return render_template('file.html', post = post)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port = 3000)
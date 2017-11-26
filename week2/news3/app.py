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
from pymongo import MongoClient
from flask import Flask, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
mongo = client.shiyanlou


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

    def add_tag(self, tag_name):
        tag_item = mongo.tags.find_one({'file_id': self.id})
        if tag_item:
            this_tags = tag_item['tags']
            if tag_name not in this_tags:
                this_tags.append(tag_name)
            else:
                return 'Already has this tag'
            mongo.tags.update_one({'file_id': self.id}, {'$set': {'tags': this_tags}})
        else:
            this_tags = [tag_name]
            mongo.tags.insert_one({'file_id': self.id, 'tags': this_tags})

    def remove_tag(self, tag_name):
        tag_item = mongo.tags.find_one({'file_id': self.id})
        if tag_item:
            this_tags = tag_item['tags']
            new_tags = this_tags.remove(tag_name)
            mongo.tags.update_one({'file_id': self.id}, {'$set', {'tags': new_tags}})
        else:
            return "Don't have this tag"

    @property
    def tags(self):
        tag_item = mongo.tags.find_one({'file_id': self.id})
        if tag_item:
            return tag_item['tags']

class Category(db.Model):
    # __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r)>' % self.name

def create_database():
    db.create_all()
    java = Category('Java')
    python = Category('python')
    file1 = File('Hello Java', java, 'File Content - Java is cool!')
    file2 = File('Hello Python', python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

def inert_mongo():
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


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
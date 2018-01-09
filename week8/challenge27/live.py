from flask import Blueprint, render_template, url_for, redirect, flash
from simpledu.forms import MessageForm
import json
from .ws import redis

live = Blueprint('live', __name__, url_prefix='/live')


@live.route('/')
def index():
    return render_template('live/index.html')


@live.route('/systemmessage', methods=['GET', 'POST'])
def systemmessage():
    form  = MessageForm()
    if form.validate_on_submit():
        redis.publish('chat', json.dumps(dict(username='System', text=form.text.data)))
        flash('系统消息发送成功', 'success')
        return redirect(url_for('admin.message'))

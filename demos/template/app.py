# -*- coding:utf-8 -*-
# @Author : yang
# @Date : 2020/07/29 14:24
# @File : app.py
# @Software : PyCharm
import os
from flask import Flask, render_template, flash, redirect, url_for, Markup

app = Flask(__name__)
app.secret_key = 'secret key'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/flash')
def just_flash():
    flash('我是一条闪现消息')
    return redirect(url_for('index'))

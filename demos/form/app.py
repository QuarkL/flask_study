# -*- coding:utf-8 -*-
# @Author : yang
# @Date : 2020/07/29 21:03
# @File : app.py
# @Software : PyCharm
from flask import Flask, render_template, flash, redirect, url_for, session, request
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
def index():
    response = ''
    if 'logged_in' in session:
        response += '[已登录]'
    else:
        response += '[未登录]'
    return render_template('index.html', response=response)


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        session['logged_in'] = True
        flash('Welcome home,%s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)

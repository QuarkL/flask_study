# -*- coding:utf-8 -*-
# @Author : yang
# @Date : 2020/07/28 12:51
# @File : app.py
# @Software : PyCharm
import click
from flask import Flask, request, redirect, url_for, make_response, session, g
import time
app = Flask(__name__)
app.secret_key = 'secret key'


@app.before_request
def get_name():
    g.name = request.args.get('name')


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = 'hello %s' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    return response


@app.route('/greet')
def greet():
    name = request.args.get('name', 'Flask')
    return 'hello' + name


@app.route('/goback/<int:year>')
def go_back(year):
    return '<h1>Welcome to %d</h1>' % (2020 - year)


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/foo')
def foo():
    return 'Foo Page<a href="%s">do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect(request.args.get('next', url_for('hello')))


if __name__ == '__main__':
    app.run()

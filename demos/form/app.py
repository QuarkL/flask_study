# -*- coding:utf-8 -*-
# @Author : yang
# @Date : 2020/07/29 21:03
# @File : app.py
# @Software : PyCharm
from flask import Flask, render_template, flash, redirect, url_for, session, request, send_from_directory
from flask_ckeditor import random_filename, CKEditor

from forms import LoginForm, UploadForm, RichTextForm
from flask_wtf import FlaskForm
import os

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['WTF_I18N_ENABLED'] = False
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['CKEDITOR_SERVE_LOCAL'] = True
ckeditor = CKEditor(app)


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
    form = LoginForm(meta={'locales': ['zh']})
    if form.validate_on_submit():
        username = form.username.data
        session['logged_in'] = True
        flash('Welcome home,%s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


@app.route('/ckeditor', methods=['GET', 'POST'])
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published!')
        return render_template('post.html', title=title, body=body)
    return render_template('ckeditor.html', form=form)

# -*- coding: utf-8 -*-
# @File    : utils.py.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-04 01:12


from flask import current_app, request, redirect, url_for


def allowed_file(filename):
    '''防止./././././'''
    return '.' in filename and filename.rsplit('.', 1)[1].lower(
    ) in current_app.config['APP_ALLOWED_IMAGE_EXTENSIONS']


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

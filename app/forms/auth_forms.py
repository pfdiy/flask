# -*- coding: utf-8 -*-
# @File    : auth_forms.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-02 10:15

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        '用户名', validators=[
            DataRequired(
                message='用户名最短4位,最长8位'), Length(
                4, 20)])
    password = PasswordField(
        '密码', validators=[
            DataRequired(
                message='密码最短8位,最长20位'), Length(
                4, 20)])
    submit = SubmitField('登录')


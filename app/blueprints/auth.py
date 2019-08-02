# -*- coding: utf-8 -*-
# @File    : auth.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 14:43

from flask import Blueprint, render_template, redirect, url_for, flash,session
from flask_login import current_user, login_user,login_required,logout_user
from app.forms.auth_forms import LoginForm
from app.models.models import Admin
from app.utils import redirect_url

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = Admin.query.first()
        if admin:
                # 验证用户名和密码
                if username == admin.username and admin.validate_password(
                        password):
                    login_user(admin)  # 登入用户
                    session.permanent = True
                    return redirect(redirect_url())
                else:
                    flash(f'用户名或密码错误')
    return render_template('admin/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

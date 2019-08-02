# -*- coding: utf-8 -*-
# @File    : extensions.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 16:19

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_qrcode import QRcode
from flask_assets import Environment,Bundle
from flask_caching import Cache

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
csrf = CSRFProtect()
migrate = Migrate()
qrcode = QRcode()
assets= Environment()
cache = Cache()


@login_manager.user_loader
def load_user(user_id):
    from app.models.models import Admin
    """使用装饰器,接受用户 id 为参数,返回对应的用户对象"""
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_message = '请先登录,在进行操作.'
login_manager.login_view ='auth.login'


css = Bundle(
    'home/css/app.css',
    'home/css/style.css',
    'home/css/swiper.min.css',
    'home/css/layui.css',
    filters='cssmin',output='assets/app.css'
)

js = Bundle(
    'home/js/swiper.min.js',
    filters = 'jsmin',output='assets/app.js'
)
assets.register('css_all',css)
assets.register('js_all',js)

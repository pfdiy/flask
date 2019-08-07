# -*- coding: utf-8 -*-
# @File    : settings.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 15:38

import os
import datetime
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', '4ea667cd2e254f71aa7a2cf2b5cab3eb')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'redis'
    CACHE_NO_NULL_WARNING =True
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_SERVE_LOCAL = False
    CKEDITOR_HEIGHT = 400
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    CKEDITOR_FILE_UPLOADER = 'index.upload_image'
    APP_UPLOAD_PATH = os.path.join(basedir, 'app/uploads')
    APP_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
    MAX_CONTENT_LENGTH = 1 * 900 * 900
    PER_PAGE = 10
    POST_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/postgres'
    CACHE_REDIS_URL = 'redis://user:123@localhost:6379/0'


class ProductionConfig(BaseConfig):
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@db/cms'
    CACHE_REDIS_URL = 'redis://user:kml7oQCKE5pXMwyz@redis:6379/0'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
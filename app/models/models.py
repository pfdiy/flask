# -*- coding: utf-8 -*-
# @File    : models.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 22:50

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    slug = db.Column(db.String(128))
    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    author = db.Column(db.String(20))
    photo = db.Column(db.String(256))
    slug = db.Column(db.String(128))
    down_url = db.Column(db.String(256))
    sources = db.Column(db.String(60))
    recommend = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cfg_url = db.Column(db.String(30))
    cfg_name = db.Column(db.String(20))
    cfg_key = db.Column(db.String(200))
    cfg_des = db.Column(db.String(200))
    cfg_beian = db.Column(db.String(50))
    cfg_copy = db.Column(db.String(50))
    cfg_add = db.Column(db.String(200))
    cfg_tel = db.Column(db.String(20))


class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slide_name = db.Column(db.String(100))
    slide_url = db.Column(db.String(300))
    slide_time = db.Column(db.DateTime, default=datetime.now, index=True)

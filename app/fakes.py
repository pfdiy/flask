# -*- coding: utf-8 -*-
# @File    : fakes.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-03 00:27


from app.models.models import Admin, Category, Site
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from faker import Faker

fake = Faker()


def fake_admin():
    admin = Admin(username='muyun')
    admin.set_password('DZSW52q07q29')
    db.session.add(admin)
    db.session.commit()


def fake_site():
    site = Site(cfg_tel='None')
    db.session.add(site)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

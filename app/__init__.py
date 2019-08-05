# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 16:01


import os
import click
from flask import Flask
from flask import render_template
from app.extensions import db, login_manager, ckeditor, csrf, migrate, \
    qrcode,assets,cache,debug
from app.models.models import Admin, Category, Post, Site
from app.blueprints.auth import auth_bp
from app.blueprints.admin import admin_bp
from app.blueprints.index import index_bp
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        # config_name = os.getenv('FLASK_CONFIG', 'development')
        config_name = os.getenv('FLASK_CONFIG', 'production')

    app = Flask('app')
    app.app_context().push()
    app.config.from_object(config[config_name])
    ckeditor.init_app(app)
    csrf.init_app(app)
    qrcode.init_app(app)
    register_errors(app)
    register_logging(app)
    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)
    register_commands(app)
    register_template_context(app)
    migrate.init_app(app, db)
    assets.init_app(app)
    cache.init_app(app)
    debug.init_app(app)
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(index_bp, url_prefix='/')


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, admin=Admin, Category=Category, Post=Post)



def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

def register_template_context(app):
    """模板上下文"""
    @app.context_processor
    def make_template_context():
        site = Site.query.first()
        return dict(site=site, Category=Category, Post=Post)


def register_commands(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=10,
                  help='Quantity of categories, default is 10.')
    def forge(category):
        """Generate fake data."""
        from app.fakes import fake_admin, fake_categories, fake_site

        db.drop_all()
        db.create_all()

        click.echo('生成管理员用户与密码.')
        fake_admin()

        click.echo('生成网站设置')
        fake_site()

        click.echo('生成 %d 条分类.' % category)
        fake_categories(category)

        click.echo('完成.')
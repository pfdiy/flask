# -*- coding: utf-8 -*-
# @File    : admin_post.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-02 21:58

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, SelectField, DateTimeField, \
    BooleanField

from app.models.models import Category


class PostForm(FlaskForm):
    """
    文章表单
    """
    title = StringField('新闻标题')
    category = SelectField('新闻分类', coerce=int, default=1)
    author = StringField('发布者')
    body = CKEditorField('新闻正文')
    photo = StringField('缩略图')
    sources = StringField('新闻来源')
    recommend = BooleanField('推荐')
    slug = StringField('文章地址',)
    down_url = StringField('下载地址')
    timestamp = DateTimeField('发布时间')
    submit = SubmitField('确认')

    # WTFForms SelectField类方法
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id,
             category.name) for category in Category.query.order_by(
                Category.name).all()]

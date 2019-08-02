# -*- coding: utf-8 -*-
# @File    : admin_cetegory.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-03 00:11

from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.models.models import Category
from flask_wtf import FlaskForm


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(1, 30)])
    slug = StringField('短网址', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('确定')

    def validata_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

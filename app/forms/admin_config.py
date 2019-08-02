# -*- coding: utf-8 -*-
# @File    : admin_config.py
# @Software: PyCharm
# Created by jianpengfei at 2019-07-09 09:24

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField


class SiteForm(FlaskForm):
    """
    网站配置表单
    """
    cfg_name = StringField('网站名称')
    cfg_url = StringField('网站地址')
    cfg_key = StringField('网站关键字')
    cfg_des = StringField('站点描述')
    cfg_beian = StringField('备案信息')
    cfg_copy = StringField('版权信息')
    cfg_add = StringField('企业地址')
    cfg_tel = StringField('企业电话')
    submit = SubmitField('确认')

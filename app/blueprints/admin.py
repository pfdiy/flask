# -*- coding: utf-8 -*-
# @File    : admin.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 17:02

from flask import url_for, render_template, request, current_app, Blueprint, redirect

from app.forms.admin_post import PostForm
from app.forms.admin_cetegory import CategoryForm
from app.forms.admin_config import SiteForm
from app.models.models import Post, Category
from app.models.models import Site
from app.extensions import db
from flask_login import login_required
import uuid
from slugify import slugify
import unittest

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def login_pro():
    pass


@admin_bp.route('/index')
def index():
    return render_template('admin/index.html')


# @admin_bp.route('/show_post/<int:post_id>')
# def show_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('admin/index_v2.html', post=post)


@admin_bp.route('/p/<slug>')
def uuid_post(slug):
    '''
    查找 Post 下 slug
    :param slug:
    :return:
    '''
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('home/post.html', post=post)


@admin_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        author = form.author.data
        photo = form.photo.data
        sources = form.sources.data
        slug = form.slug.data
        down_url = form.down_url.data
        recommend = form.recommend.data
        timestamp = form.timestamp.data
        category = Category.query.get(form.category.data)
        post = Post(
            title=title,
            photo=photo,
            author=author,
            down_url=down_url,
            sources=sources,
            recommend=recommend,
            slug=TestSlugification.test_extraneous_seperators(slug),
            body=body,
            timestamp=timestamp,
            category=category)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post_list', post_id=post.id, slug=slug))
    return render_template('admin/add_post.html', form=form)


class TestSlugification(unittest.TestCase):
    def test_extraneous_seperators(self):
        """url 生成为 uuid 取前 12 位"""
        uid = str(uuid.uuid4().hex)
        suid = ''.join(uid.split('-'))
        txt = suid[0:12]
        r = slugify(txt)
        return (r)
        print(r)


@admin_bp.route('/show_post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.timestamp = form.timestamp.data
        post.author = form.author.data
        post.sources = form.sources.data
        post.photo = form.photo.data
        post.slug = form.slug.data
        post.down_url = form.down_url.data
        post.recommend = form.recommend.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        return redirect(url_for('.post_list', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.timestamp.data = post.timestamp
    form.author.data = post.author
    form.down_url.data = post.down_url
    form.sources.data = post.sources
    form.category.data = post.category_id
    form.photo.data = post.photo
    form.slug.data = post.slug
    form.recommend.data = post.recommend
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/show_post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.post_list'))


@admin_bp.route('/post_list')
def post_list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template(
        'admin/post_list.html',
        posts=posts,
        pagination=pagination)


@admin_bp.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        slug = form.slug.data
        category = Category(name=name)
        category = category(slug=slug)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.category_list', category_id=category.id))
    return render_template('admin/add_category.html', form=form)


@admin_bp.route('/category_list')
def category_list():
    categorys = Category.query.order_by().all()
    return render_template('admin/category_list.html', categorys=categorys)


@admin_bp.route('/category/<int:category_id>')
def show_category(category_id):
    """查询出分类下所有文章并分页"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc(
    )).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('admin/post_list.html', category=category,
                           pagination=pagination, posts=posts)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('.category_list'))


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        db.session.commit()
        return redirect(url_for('.category_list', category_id=category.id))
    form.name.data = category.name
    form.slug.data = category.slug
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/admin_cfg/<int:site_id>', methods=['GET', 'POST'])
def admin_cfg(site_id):
    form = SiteForm()
    site = Site.query.get_or_404(site_id)
    if form.validate_on_submit():
        site.cfg_name = form.cfg_name.data
        site.cfg_url = form.cfg_url.data
        site.cfg_key = form.cfg_key.data
        site.cfg_des = form.cfg_des.data
        site.cfg_beian = form.cfg_beian.data
        site.cfg_copy = form.cfg_copy.data
        site.cfg_add = form.cfg_add.data
        site.cfg_tel = form.cfg_tel.data
        db.session.commit()
        return redirect(url_for('.admin_cfg', site_id=site.id))
    form.cfg_name.data = site.cfg_name
    form.cfg_url.data = site.cfg_url
    form.cfg_key.data = site.cfg_key
    form.cfg_des.data = site.cfg_des
    form.cfg_beian.data = site.cfg_beian
    form.cfg_copy.data = site.cfg_copy
    form.cfg_add.data = site.cfg_add
    form.cfg_tel.data = site.cfg_tel
    return render_template('admin/admin_config.html', form=form)

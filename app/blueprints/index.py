# -*- coding: utf-8 -*-
# @File    : index.py
# @Software: PyCharm
# Created by jianpengfei at 2019-06-29 17:27


from flask import Blueprint, render_template, current_app, request, \
    url_for, send_file, send_from_directory
from flask_ckeditor import upload_success, upload_fail
from app.utils import allowed_file
from app.models.models import Post, Category
from app.extensions import qrcode,cache
import os, uuid
from flask_login import login_required

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
@cache.cached(timeout=10 * 60)
def show_category():
    category = Category.query.get_or_404(1)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc(
    )).paginate(page, per_page=per_page)
    posts = pagination.items
    category01 = Category.query.get_or_404(2)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pagination01 = Post.query.with_parent(category01).order_by(
        Post.timestamp.desc(
        )).paginate(page, per_page=per_page)
    posts01 = pagination01.items
    category02 = Category.query.get_or_404(3)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']
    pagination02 = Post.query.with_parent(category02).order_by(
        Post.timestamp.desc(
        )).paginate(page, per_page=per_page)
    posts02 = pagination02.items
    return render_template('home/index.html', category=category,
                           pagination=pagination, posts=posts,
                           category01=category01, posts01=posts01,
                           pagination01=pagination01, category02=category02,
                           posts02=posts02, pagination02=pagination02)


@index_bp.route('/p/<slug>')
@cache.cached(timeout=10 * 60)
def uuid_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('home/post.html', post=post)


@index_bp.route('/category/<slug>')
@cache.cached(timeout=10 * 60)
def slug_category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc(
    )).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('home/category_list.html', category=category,
                           pagination=pagination, posts=posts)


@index_bp.route('/category_list')
@cache.cached(timeout=10 * 60)
def category_list():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('home/category_list.html', posts=posts,
                           pagination=pagination)


@index_bp.route('/xiazai')
@login_required
@cache.cached(timeout=10 * 60)
def xiazai():
    return render_template('home/down_post.html')


@index_bp.route("/qrcode", methods=["GET"])
def get_qrcode():
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")


@index_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['APP_UPLOAD_PATH'], filename)


@index_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('只允许上传 png jpg jpeg')
    filename = random_filename(f.filename)
    f.save(os.path.join(current_app.config['APP_UPLOAD_PATH'], filename))
    url = url_for('.get_image', filename=filename)
    return upload_success(url, filename)


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

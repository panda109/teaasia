# app/main/views.py

from flask import render_template, session, redirect, url_for, current_app, jsonify, request
from flask_login import login_required, current_user
import random, datetime
from .. import db
from ..models import User, Story, Post, Product
from ..email import send_email
from . import main
from .forms import NameForm
from ..models import Catalog

@main.route('/message')
@login_required
def message():
    catalogs = Catalog.get_all()
    posts = Post.get_last5()
    return render_template('message.html', catalogs=catalogs,posts=posts)

@main.route('/post/', methods=['GET'])
def post_message():
    ret_data = {"value": request.args.get('messageValue')}
    post = Post()
    post.constain = ('%.200s' % ret_data['value'])
    post.author = current_user.username
    post.post_datetime = datetime.datetime.utcnow()
    db.session.add(post)
    db.session.commit()
    #posts = Post.query.order_by(Post.post_datetime.desc()).filter_by()
    return jsonify({'value' : 'Succesed.'})

@main.route('/get/', methods=['GET'])
def get_message():
    posts = Post.get_last5()
    json_list = [i.serialize for i in posts]
    return jsonify(json_list)

@main.route('/')
def index():
    
    # query catalog into index.html
    catalogs = Catalog.get_all()
    stories = Story.get_all()
    posts = Post.get_last5()
    products = Product.get_last3()
    random_items = random.sample(population=stories, k=5)
    return render_template('index.html', catalogs=catalogs, stories=random_items, posts = posts, products = products)

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed! Current user: {}'.format(current_user.username)

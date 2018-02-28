# app/main/views.py

from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required, current_user
import random
from .. import db
from ..models import User, Story
from ..email import send_email
from . import main
from .forms import NameForm
from ..models import Catalog


@main.route('/')
def index():
    
    # query catalog into index.html
    catalogs = Catalog.get_all()
    stories = Story.get_all()
    random_items = random.sample(population=stories, k=5)
    return render_template('index.html', catalogs=catalogs, stories=random_items)

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed! Current user: {}'.format(current_user.username)

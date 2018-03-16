# app/main/views.py

import requests
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from flask import Flask, request
from flask import json
from .. import db
from app.interactive import interactive
from ..models import  Catalog, Interactive
from .. import csrf
from forms import InteractiveForm
from flask_login import login_user, logout_user, login_required, current_user

@interactive.route("/create_order", methods=['GET', 'POST'])
@login_required
def create_order():
    """Return page showing all the products has to offer"""

    form = InteractiveForm()
    if form.validate_on_submit():
        interactive = Interactive(
        car_type=form.car_type.data,
        tour_type=form.tour_type.data,
        tour_guide=form.tour_guide.data,
        total_price=request.form.get('total'),
        userid = current_user.id)
        db.session.add(interactive)
        db.session.commit()
        flash('Add order successfull.')
        return redirect(url_for('interactive.list_order'))
    # pre setting value
    catalogs = Catalog.get_all()
    return render_template('interactive/create_order.html', form=form,
                            catalogs=catalogs, title="Add Interactive") 
    
@interactive.route("/list_order", methods=['GET'])
@login_required
def list_order():
    
    
    
    
    catalogs = Catalog.get_all()
    return render_template('interactive/list_order.html',
                        catalogs=catalogs, title="Add Interactive") 
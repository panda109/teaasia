# app/main/views.py

import requests
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from flask import Flask, request
from flask import json
from .. import db
from app.interactive import interactive
from ..models import  Catalog, Interactive, Car_type, Tour_type
from .. import csrf
from forms import InteractiveForm
from flask_login import login_user, logout_user, login_required, current_user


@interactive.route("/pay/<int:id>", methods=['GET'])
@login_required
def pay(id):
    
    interactive = Interactive.query.get_or_404(id)
    catalogs = Catalog.get_all()
    return render_template('interactive/pay_tour.html',
                        catalogs=catalogs, interactive = interactive, title="Pay Interactive_order") 

@interactive.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    """Return page showing all the products has to offer"""

    form = InteractiveForm()
    if form.validate_on_submit():
        rows = Interactive.query.filter_by(userid = current_user.id, comfirmed = False).count()
        if (rows == 5):
            flash("Your couldn't add tours more than 5 times.")
            return redirect(url_for('interactive.list'))
        interactive = Interactive(
        car_type=Car_type.query.filter_by(value=str(form.car_type.data.value)).first().id,
        tour_type=Tour_type.query.filter_by(value=str(form.tour_type.data.value)).first().id,
        tour_guide=form.tour_guide.data,
        total_price=request.form.get('total'),
        userid = current_user.id)
        db.session.add(interactive)
        db.session.commit()
        flash('Add order successfull.')
        
        
        return redirect(url_for('interactive.list'))
    # pre setting value
    catalogs = Catalog.get_all()
    return render_template('interactive/create_tour.html', form=form,
                            catalogs=catalogs, title="Add Interactive") 

@interactive.route("/remove/<int:id>", methods=['GET'])
@login_required
def remove(id):
    
    interactive = Interactive.query.get_or_404(id)
    db.session.delete(interactive)
    db.session.commit()
    interactives = Interactive.query.filter_by(userid = current_user.id, comfirmed = False)  
    catalogs = Catalog.get_all()
    return render_template('interactive/list_tour.html',
                        catalogs=catalogs, interactives = interactives, title="Remove Interactive_order") 
    
@interactive.route("/list", methods=['GET'])
@login_required
def list():
    
    interactives = Interactive.query.filter_by(userid = current_user.id, comfirmed = False)
    
    catalogs = Catalog.get_all()
    return render_template('interactive/list_tour.html',
                        catalogs=catalogs, interactives = interactives, title="List Interactive_order") 
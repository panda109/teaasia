# app/main/views.py

import requests
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from flask import Flask, request
from flask import json
from app.interactive import interactive
from ..models import Product, Order, Order_detail, Catalog
from .. import csrf
from forms import InteractiveForm
from flask_login import login_user, logout_user, login_required, current_user

@interactive.route("/create_order", methods=['GET', 'POST'])
def create_order():
    """Return page showing all the products has to offer"""

    form = InteractiveForm()
    if form.validate_on_submit():
        print form.car_type.data
        print form.tour_type.data
        print form.tour_guide.data
        print request.form.get('total')
        print current_user.id
        # redirect to the departments page
        return redirect(url_for('interactive.create_order'))
    # pre setting value
    catalogs = Catalog.get_all()
    return render_template('interactive/interactive.html', form=form,
                            catalogs=catalogs, title="Add Interactive") 

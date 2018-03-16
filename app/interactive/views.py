# app/main/views.py

import requests
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from flask import Flask, request
from flask import json
from app.interactive import interactive
from ..models import Product, Order, Order_detail, Catalog
from .. import csrf

@interactive.route("/add_interactive", methods=['GET', 'POST'])
def add_interactive():
    """Return page showing all the products has to offer"""

    form = interactive.Form()
    if form.validate_on_submit():
        interactived = interactive(catalog_name=form.name.data)
        
        
        
        
        db.session.add(catalog)
        db.session.commit()
        # redirect to the departments page
        return redirect(url_for('interactive.add_interactive'))
    # pre setting value
    catalogs = Catalog.get_all()
    return render_template('interactive/interactive.html', form=form,
                            catalogs=catalogs, title="Add Interactive") 

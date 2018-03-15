# app/main/views.py

import requests
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from flask import Flask, request
from flask import json
from app.interactive import interactive
from ..models import Product, Order, Order_detail, Catalog
from .. import csrf

@interactive.route("/get", methods=['GET'])
def get():
    catalogs = Catalog.get_all()
    # pre setting value
    return render_template('interactive/order.html', catalogs=catalogs)
    
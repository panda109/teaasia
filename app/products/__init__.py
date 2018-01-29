# app/product/__init__.py  (Blueprint creation)

from flask import Blueprint

products = Blueprint('products', __name__)

# can use from main import views
from . import views, errors

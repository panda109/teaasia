# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Product

class AddProductFrom(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    common_name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    imurl = StringField('ImageURL', validators=[DataRequired()])
    flesh_color = StringField('Flesh_Color')
    rind_color = StringField('Rind_Color')
    available = StringField('Available', validators=[DataRequired()])
    catalog_id = StringField('Catalog', validators=[DataRequired()])
    submit = SubmitField('Submit')

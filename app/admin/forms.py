# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField 
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Product, Catalog, Role
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form
from flask_uploads import UploadSet, IMAGES
images = UploadSet('images', IMAGES)


class ChangeCatalogForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    common_name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    upload = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    # imgurl = StringField('FileName')
    color = StringField('Color')
    size = StringField('Size')
    catalog_id = QuerySelectField(query_factory=lambda: Catalog.query.all(), get_label="catalog_name")
    available = BooleanField('Available', default=True)
    submit = SubmitField('Submit')


class ChangeUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    add = StringField('Address', validators=[DataRequired()])
    confirmed = BooleanField('Confirmed', default=True)
    submit = SubmitField('Submit')


class OrderForm(FlaskForm):
    # add ship_status
    submit = SubmitField('Submit')

    
class OrderdetailForm(FlaskForm):
    # edit number and price
    submit = SubmitField('Submit')

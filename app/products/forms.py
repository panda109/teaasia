# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField 
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Product,Catalog
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form
from flask_uploads import UploadSet, IMAGES
images = UploadSet('images', IMAGES)
class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    common_name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    upload = FileField('Image', validators=[FileRequired(),FileAllowed(images, 'Images only!')])
    imgurl = StringField('ImgURL')
    color = StringField('Color')
    size = StringField('Size')
    catalog_id = QuerySelectField(query_factory=lambda: Catalog.query.all(),get_label="catalog_name")
    available = BooleanField('Available', default=True)
    submit = SubmitField('Submit')

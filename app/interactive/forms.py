# app/admin/forms.py

#from flask_wtf import FlaskForm
from app import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form
from wtforms.widgets import TextArea

class InteractiveForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    car_type = SelectField('Car_type' , choices=[('Small Car(5 people)', 1), ('Big Car(7 people)', 2), ('Large Car(9 people)', 3), ('Vito(9 people)', 4)])
    tour_type = SelectField('Tour_type' , choices=[('8 hours)', 1), ('10 hours', 2), ('2 days', 3), ('3 days', 4), ('4 days', 5), ('5 days', 6)])
    tour_guide = BooleanField('Tour_guide', default=False)
    submit = SubmitField('Submit')
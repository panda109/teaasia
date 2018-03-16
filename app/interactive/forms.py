# app/admin/forms.py

#from flask_wtf import FlaskForm
from app import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form
from wtforms.widgets import TextArea


class InteractiveForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    car_type = SelectField('Car_type' , choices=[("1",'Wish, Previa(5 people)'), ("2",'Wish, Previa(7 people)'), ("3",'Wolks vagon(9 people)'), ("4",'Benz Vito(9 people)')])
    tour_type = SelectField('Tour_type' , choices=[("1",'8 hours'), ("2",'10 hours'), ("3",'2 days'), ("4",'3 days'), ("5",'4 days'), ("6",'5 days'), ("7",'6 days'), ("8",'7 days')])
    tour_guide = BooleanField('Tour_guide(English)', default=False)
    submit = SubmitField('Submit')
    
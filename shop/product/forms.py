from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subscribe = TextAreaField('Subscribe', validators=[DataRequired()])
    img_file = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add a new product')
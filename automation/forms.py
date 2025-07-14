from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Ambition(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    ambition = StringField('Ambition', validators=[DataRequired()])
    submit = SubmitField('Submit')

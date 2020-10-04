from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class PostForm(FlaskForm):
	title = StringField('Title:', validators=[DataRequired()])
	content = TextField('Content:', validators=[DataRequired()])
	submit = SubmitField('Post')

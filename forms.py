# ---------------------------- IMPORTED MODULES------------------------------- #
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField


# ---------------------------- WTForms------------------------------- #
# class CreatePostForm(FlaskForm):
# 	title = StringField("Blog Post Title", validators=[DataRequired()])
# 	subtitle = StringField("Subtitle", validators=[DataRequired()])
# 	img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
# 	body = CKEditorField("Blog Content", validators=[DataRequired()])
# 	submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = EmailField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Register")


class LoginForm(FlaskForm):
	email = EmailField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Register")


class CommentForm(FlaskForm):
	comment = CKEditorField("Comment", validators=[DataRequired()])
	submit = SubmitField("Submit Comment")


class GetInTouch(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = EmailField("Email", validators=[DataRequired(), Email()])
	phone = TelField('Phone Number', validators=[DataRequired()])
	message = StringField("Message", validators=[DataRequired()])
	submit = SubmitField("Send Request")

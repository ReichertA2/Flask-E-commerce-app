from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
# from jinja2.utils import markupsafe





#Form section
class LoginForm(FlaskForm):
    # field name = DataTypeField('LABEL', validators=[LIST OF validators])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password Must match')])
    submit = SubmitField('Register')

# MUST BE LIKE THIS!! VALIDATE_FIELDNAME
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
            #SELECT * FROM user WHERE email = ???
        if same_email_user:
            raise ValidationError('Email is Already in Use')
        


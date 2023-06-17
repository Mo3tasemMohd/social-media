
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField(
        'Sign Up'
    )

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Login'
    )



class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
        ]
    )

    content = StringField(
        'Content',
        validators=[
            DataRequired()
        ]
    )

    privacy = SelectField('Privacy', 
    choices=[('only_me', 'Only Me'), ('friends', 'Friends'), ('public', 'Public')],
    default='public'
    )
    submit = SubmitField(
        'Post'
    )

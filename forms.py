from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=200)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=40)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=40)])

class LoginForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])

class FeedbackForm(FlaskForm):
    """Form for adding feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("Enter content", validators=[InputRequired(), Length(min=5)])
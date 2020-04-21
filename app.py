from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def goto_register():
    """Meant to redirect user to /register"""
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_page():
    """Form for registering a user & handle this logic"""
    form = RegisterForm()

    return render_template('home-reg.html', form=form)
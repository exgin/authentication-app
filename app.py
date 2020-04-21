from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import LoginForm, RegisterForm, FeedbackForm

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

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{username}")
    else:
        return render_template('home-reg.html', form=form)

@app.route('/users/<username>') 
def show_secret(username):
    """Only logged in users can view this part of the site, changed to show the
    details of a user, expect their password of course
    """
    user = User.query.get_or_404(username)

    # you have to be logged in & THE SAME username as the user logged in
    if "username" not in session or username != session['username']:
        raise Unauthorized()


    return render_template('secret.html', user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Only a authenticated user can delete his/her own account"""

    # we can't have not logged in users sending delete POST requests to this route
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    flash("Account deleted")
    return redirect("/register")

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """Add feedback & handle its logic"""

    # must be logged into the session
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()
        flash("Feedback created!")
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback-form.html", form=form)


@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    # remember when editing a form, have to set the object/model of the db to the form
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback-edit.html", form=form, feedback=feedback)



@app.route('/login', methods=["GET", "POST"])
def login():
    """Allows our user to login & shows login form"""
    form = LoginForm()
    
    # now we have to authenticate & compare user's pw to our hashed pw
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username,password)

        if user:
            # session allows us to stay logged in
            session["username"] = user.username
            return redirect(f"/users/{username}")
        else:
            # handle an error
            form.username.errors = ["A wrong username/password was entered"]
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    """Allows our user to logout"""

    session.pop("username")
    return redirect("/login")
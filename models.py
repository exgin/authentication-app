from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Base user"""
    __tablename__ = "users"

    username = db.Column(db.String(20), 
                         nullable=False, 
                         unique=True, primary_key=True)
    password = db.Column(db.Text, 
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False)
    first_name = db.Column(db.String(30), 
                          nullable=False)
    last_name = db.Column(db.String(30), 
                          nullable=False)

    # Creating our user password
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Handle registering a user with a hashed password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

        # now within the app.py all we have to do is commit, since we added .add here
        db.session.add(user)
        return user

    # Authenticating our login
    @classmethod
    def authenticate(cls, username, password):
        """Handle authenticating a user to specific parts of a website"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False
    

class Feedback(db.Model):
    """Feedback model"""
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, 
                primary_key=True, 
                autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                      nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )

    users = db.relationship('User', backref='feedback', cascade="all,delete")
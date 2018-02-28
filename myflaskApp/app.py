from flask import Flask, render_template, flash, url_for, session, request, logging, redirect
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:January@2018@localhost/myFlaskApp'
db = SQLAlchemy(app)
app.secret_key = 'my unobvious secret key'


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


Articles = Articles()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

@app.route('/process/<name>')
def process(name):
	reverse.delay(name)
	return 'I sent a Async request'

@celery.task(name='tasks.reverse')
def reverse(string):
	return string[::-1]


class RegisterForms(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForms (request.form)
    if request.method == 'POST' and form.validate ():
        username = str(form.username.data)
        email = str(form.email.data)
        password = sha256_crypt.encrypt(str(form.password.data))
        result = User (request.form['username'], request.form['email'], request.form['password'])
        db.session.add (result)
        db.session.commit ()
        flash('You are now registered', 'success')
        return redirect (url_for ('index'))


    return render_template ('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, flash, url_for, session, request, logging, redirect, jsonify, make_response
from data import Articles
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_celery import make_celery
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
import uuid
from werkzeug.security import generate_password_hash, check_password_hash 
import pdfkit
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

twitter_blueprint = make_twitter_blueprint(api_key='', api_secret='')
github_blueprint = make_github_blueprint(client_id='', client_secret='')

app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')
app.register_blueprint(github_blueprint, url_prefix='/github_login')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:January@2018@localhost/myFlaskApp'
db = SQLAlchemy(app)
app.secret_key = 'my obvious secret key'

#config1 = pdfkit.configuration(wkhtmltopdf='your exe file')
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    course = db.relationship('Courses', backref='owner', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Courses(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(200),unique=True, nullable=False)
	title = db.Column(db.String(200),unique=True, nullable=False)
	person_id = db.Column(db.String(80), db.ForeignKey('user.username'),
        nullable=False)



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
	
@app.route('/<user>/<course>/<url>')
def send_pdf(user, course, url):
	send.delay(user, course, url)
	
	return "Your request has been send to Admin for Approval"

@celery.task(name='celery_mail_pdf.send')
def send(user, course, url):
	rendered = render_template('pdf_template.html', name=name, location=location)
	pdf = pdfkit.from_string(rendered,False,configuration = config1)
	
	thesender = User.query.filter(User.username == user).first()
	
	msg = Message('Hello', sender = [thesender.email], recipients = [athul8raj@gmail.com])
	msg.attach("NewCourses.pdf","application/pdf", pdf)
	mail.send(msg)	


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
        password = generate_password_hash(str(form.password.data),method='sha512')
        result = User (request.form['username'], request.form['email'], request.form['password'])
        db.session.add (result)
        db.session.commit ()
        flash('You are now registered', 'success')
        return redirect (url_for ('index'))


    return render_template ('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']
		
		result = User.query.filter_by(username = username).first()
		
		if result:
			if password_candidate == result.password:
				session['logged_in'] = True
				session['username'] = username
				
				flash('You are now logged in', 'success')
				return redirect(url_for('courses'))
			else:
				error = 'Password not valid'
				app.logger.info('Password not valid')
				return render_template('login.html', error = error)
		else:
			error = 'Username not found'
			return render_template('login.html', error = error)
			
	return render_template('login.html')
	
@app.route('/twitter')
def twitter_login():
	if not twitter.authorized:
		return redirect(url_for('twitter.login'))
	account_info = twitter.get('account/settings.json')
	
	if account_info.ok:
		session['logged_in'] = True
		account_info_json = account_info.json()
		session['username'] = account_info_json['screen_name']
		return redirect(url_for('courses'))
	
	return '<h2>Request failed</h2>'

@app.route('/github')
def github_login():
	if not github.authorized:
		return redirect(url_for('github.login'))
	account_info = github.get('/user')
	
	if account_info.ok:
		session['logged_in'] = True 
		account_info_json = account_info.json()
		session['username'] = account_info_json['login']
		return redirect(url_for('courses'))
	
	return '<h2>Request failed</h2>'

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))
	
@app.route('/courses')
def courses():
	return render_template('courses.html')

@app.route('/addCourses', methods=['POST'])
def create_course():
	data = request.get_json()
	create_course = Courses(url=data['url'],title=data['title'], person_id=data['username'])
	db.session.add(create_course)
	db.session.commit()
	return jsonify({'message': 'Your course has been added successfully!'})

@app.route('/addCourses/<person_id>', methods=['GET'])
def get_all_courses(person_id):
	data = Courses.query.filter_by(person_id=person_id).first()
	
	output = []	
	course_data = {}
	course_data['url'] = data.url
	course_data['title'] = data.title
	output.append(course_data)
	
	return jsonify({'courses': output})
	
@app.route('/addCourses/<person_id>', methods=['DELETE'])
def del_course(person_id):
	data = Courses.query.filter_by(person_id=person_id).first()
	if not data:
		return jsonify ({'message': 'Course not found'})
	db.session.delete(data)
	db.session.commit()
	return jsonify({'message':'Course is deleted'})
	
@app.route('/addCourses/<person_id>', methods=['PUT'])
def promote_course(person_id):
	data = Courses.query.filter_by(person_id=person_id).first()
	if not data:
		return jsonify({'message': 'Course not found'})
	data.title = 'Flask' #for now
	db.session.commit()
	return jsonify ({'message':'Changes done successfully'})



if __name__ == '__main__':
    app.run(debug=True)

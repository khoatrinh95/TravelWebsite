import csv
import re

import bcrypt
from flask import Flask, session, redirect, url_for, request
from flask import render_template, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = "SOEN287"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password


@login_manager.user_loader
def load_user(username):
    user = find_user(username)
    if user:
        user.password = None
    return user


class loginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField('login')


class commentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[InputRequired()])
    submit = SubmitField('Submit')


def find_user(username):
    with open('data/users.csv') as f:
        for user in csv.reader(f):
            if username == user[0]:
                return User(*user)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect('/')


@app.route('/')
def base():
    return render_template("base.html")


d = []
with open('data/countries') as f:
    countries = f.readlines()
for line in countries:
    list = line.split(' ')
    d.append(list)
with open('data/backgrounds') as g:
    background = g.readlines()
with open('data/continents') as h:
    continent = h.readlines()


@app.route('/destinations')
def destination():
    asia = [x[0] for x in d[0:5]]
    europe = [x[0] for x in d[5:11]]
    namer = [x[0] for x in d[11:13]]
    samer = [x[0] for x in d[13:18]]
    australia = [x[0] for x in d[18:21]]
    africa = [x[0] for x in d[21:26]]
    countries_list = [asia, europe, namer, samer, australia, africa]
    return render_template("destinations.html", countries=countries_list, continent=continent, background=background)


@app.route('/checklist')
def checklist():
    with open('data/beach') as f:
        beach = f.readlines()
    with open('data/outdoors') as g:
        outdoors = g.readlines()
    with open('data/sightseeing') as h:
        sight = h.readlines()
    with open('data/essentials') as i:
        essentials = i.readlines()
    return render_template("checklist.html", beach=beach, outdoors=outdoors, sight=sight, essentials=essentials)


@app.route('/tips')
def tips():
    return render_template("tips.html")


@app.route('/article/<a>', methods=["GET", "POST"])
def article(a):
    list = []
    file = ('data/' + a)
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        item = line.split('*')
        list.append(item)
    list1 = [x[1] for x in list]
    return render_template("article.html", list=list1)


@app.route('/searchpage', methods=['POST'])
def search_page():
    input = r'\b'+request.form['input'].lower()+r'\b'
    filesToOpen = [False,False, False, False]
    with open('data/airbnb') as f:
        lines = f.readlines()
    title=lines[0].lower()
    desc=lines[8].lower()
    if re.search(input,title) or re.search(input,desc):
        filesToOpen[1] = True
    with open('data/airport') as f:
        lines = f.readlines()
    title = lines[0].lower()
    desc = lines[8].lower()
    if re.search(input,title) or re.search(input,desc):
        filesToOpen[0] = True
    with open('data/flight') as f:
        lines = f.readlines()
    title = lines[0].lower()
    desc = lines[8].lower()
    if re.search(input,title) or re.search(input,desc):
        filesToOpen[3] = True
    with open('data/skin') as f:
        lines = f.readlines()
    title = lines[0].lower()
    desc = lines[8].lower()
    if re.search(input,title) or re.search(input,desc):
        filesToOpen[2] = True
    return render_template('searchpage.html', list = filesToOpen)


@app.route('/country/<a>', methods=["GET", "POST"])
def country(a):
    photo = ""
    for x in d:
        if x[0] == a:
            photo = x[1].strip('\n')
            break
    form = commentForm()
    if form.validate_on_submit():
        with open('data/comments', 'a+') as f:
            f.write(form.comment.data)
            f.write('\n')
        return redirect(url_for('country', a=a))
    with open('data/comments') as g:
        lines = g.readlines()
    return render_template("country.html", form=form, comment=lines, country=a, photo=photo)


@app.route('/aboutme')
def aboutme():
    return render_template("aboutme.html")


if __name__ == '__main__':
    app.run()

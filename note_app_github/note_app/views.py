from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from .models import User, Note
from . import app, lm
from .forms import LoginForm, SignupForm, AddNoteForm

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("login successful")
            return redirect(url_for('home'))
        flash("Incorrect password or email")
    return render_template("login.html", form = form)
@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new = User(username = form.username.data, email = form.email.data, password = form.password.data)
        new.save()
        flash("registration was successful")
        return redirect(url_for('login'))

    return render_template("signup.html", form = form)
@login_required
@app.route("/home", methods = ['POST', 'GET'])
def home():
    notes = Note.query.filter_by(user_id = current_user.id)
    return render_template("home.html", notes = notes)
@login_required
@app.route("/add", methods = ['POST', 'GET'])
def add():
    form = AddNoteForm()
    if form.validate_on_submit():
        new = Note(title = form.title.data, content = form.content.data, user_id = current_user.id)
        new.save()
        flash("Note created successfully")
        return redirect(url_for('home'))
    return render_template("new.html", form = form)

@login_required
@app.route("/view/<id>")
def view(id):
    notes = Note.query.filter_by(user_id = current_user.id)
    note = Note.query.get(id)
    return render_template("note.html", note = note, notes = notes)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
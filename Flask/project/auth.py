from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('project/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # Check if user input matches existing credentials
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # hash the password and check against that one existing, as well as the email provided
    if not user or not check_password_hash(user.password, password):
        flash('Please check login details and try again')
        # if something is wrong then reload the page
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('project/signup.html')


# part of validation and adding user to db
@auth.route('/signup', methods=['POST'])
def signup_post():
    # Fields to be filled by user
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # get the user by email if that already exists via filtering
    user = User.query.filter_by(email=email).first()

    # If user exists then reload page
    if user:
        # on request of failed signuo the user will be notified
        flash('Email address already exists')
        # redirect user to try again on same page
        return redirect(url_for('auth.signup'))

    # create user with the input provided
    # and hash the password using 'sha' (bad practice saving in plain-text)
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add user to db
    db.session.add(new_user)
    db.session.commit()

    # Redirect to login page after successful sign up
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required # doesn't make sense to logout if the user is not logged in
def logout():
    logout_user()
    return redirect(url_for('main.index'))

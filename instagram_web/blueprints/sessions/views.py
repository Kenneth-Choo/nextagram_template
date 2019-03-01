from flask import Flask, app, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from instagram_web.util.oauth_helpers import *

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates/sessions')

# google login
@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    token = oauth.google.authorize_access_token()
    get_email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

    # check if email exists in database
    email = User.get_or_none(User.email==get_email)

    if email:
        email_login = User.get(User.email==get_email)
        login_user(email_login)
        flash("Successfully logged in", "success")
        return render_template('home.html')
    else:
        flash("User does not exist. Please try again with a valid email!", "danger")
        return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/login')
def new():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('login.html')

# site login
@sessions_blueprint.route('/', methods=['POST'])
def login():
    user = User.get_or_none(User.name==request.form['username_sign_in'])

#  check if user exist
    if user:
        password_check = request.form['password_sign_in']
        result = check_password_hash(user.password, password_check)

  #    check if user & password match
        if result:
            user_login = User.get(User.name==request.form['username_sign_in'])
            # Flask-login - login the user
            login_user(user_login)
            flash("You have successfully logged in!", "success")
            # Add in session key
            return render_template('home.html')
        else:
            flash("Login Unsuccesful! Please check username and password", "danger")
            return redirect(url_for('sessions.new'))
    else:
        flash("Login Unsuccesful! Please check username and password", "danger")
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/')
@login_required
def logout():
    logout_user()
    flash("You have logged out!", "success")
    return redirect(url_for('sessions.new'))

from flask import Flask, app, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates/sessions')


@sessions_blueprint.route('/login')
def new():
    return render_template('login.html')


@sessions_blueprint.route('/',methods=['POST'])
def check_sign_in():
   user = User.get_or_none(User.name==request.form['username_sign_in'])
   if user:
       password_to_check = request.form['password_sign_in']
       result = check_password_hash(user.password, password_to_check)
       if result:
           user_login = User.get(User.name==request.form['username_sign_in'])
           # Flask-login - login the user
           login_user(user_login)
           flash("You have successfully logged in!", "success")
           # Add in session key
           return redirect(url_for("users.new", username=request.form['username_sign_in']))
       else:
           flash("Login Unsuccesful! Please check username and password", "danger")
           return render_template('login.html')
   else:
        flash("Login Unsuccesful! Please check username and password", "danger")
        return render_template('login.html')

@sessions_blueprint.route('/logout')
def logout():
    return

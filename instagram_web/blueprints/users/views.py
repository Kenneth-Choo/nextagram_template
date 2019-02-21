from flask import Flask, app, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['password_sign_up']
    hashed_password = generate_password_hash(user_password)
    user_sign_up = User(name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
    password=hashed_password)
    if user_sign_up.save():
        flash("Successfully signed up!")
        return redirect(url_for('users.new'))
    else:
        return render_template('new.html', name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
        password=request.form['password_sign_up'])


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

import os
import config
from flask import Flask, render_template, redirect, request, flash, url_for
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CsrfProtect

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CsrfProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/sign_up")
def sign_up():
   return render_template('sign_up.html')

@app.route("/sign_up_form", methods=['POST'])
def sign_up_form():
    user_password = request.form['password_sign_up']
    hashed_password = generate_password_hash(user_password)
    user_sign_up = User(name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
    password=hashed_password)

    if user_sign_up.save():
        flash("Successfully signed up!")
        return redirect(url_for('sign_up'))
    else:
        return render_template('sign_up.html', name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
        password=request.form['password_sign_up'])

if __name__ == '__main__':
    app.run(debug=True)
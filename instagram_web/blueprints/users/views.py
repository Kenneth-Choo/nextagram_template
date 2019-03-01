from app import app
from flask import Flask, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from models.image import Image
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.s3_helpers import upload_file_to_s3, allowed_file


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

# create new user
@users_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('users/new.html')

# upload new user info to db
@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['password_sign_up']
    hashed_password = generate_password_hash(user_password)
    user_sign_up = User(name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
    password=hashed_password)
    
    if user_sign_up.save():
        flash("Successfully signed up!", "success")
        return redirect(url_for('users.new'))
    else:
        flash("Please try again", "error")
        return render_template('users/new.html', name=request.form['username_sign_up'], email=request.form['email_sign_up'], 
        password=request.form['password_sign_up'])

# render profile page
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    image_list = Image.select().join(User).where(User.name == current_user.name)
    return render_template('users/show.html', username=username, image_list=image_list)

# index
@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

# render profile edit
@users_blueprint.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    if current_user.is_authenticated:
        return render_template('users/edit.html', id=id)
    else:
        flash("Please sign in to edit profile", "danger")
        return redirect(url_for('sessions.new'))

# edit profile info
@users_blueprint.route('/<int:id>', methods=['POST'])
def update(id):
    user_update = User.update(name=request.form['username_update'], email=request.form['email_update'], 
                  password=generate_password_hash(request.form['password_update'])).where(User.id==id).execute()

    if current_user.is_authenticated:
        if user_update:
            flash("Profile successfully updated", "success")
            return render_template('users/edit.html')
        else:
            flash("An error occurred, please try again", "danger")
            return render_template('users/edit.html')
    else:
        flash("Please sign in to edit profile", "danger")
        return redirect(url_for('sessions.new'))


# upload profile picture
@users_blueprint.route('/<int:id>/edit', methods=['POST'])
def upload_pic(id):
    # check request.files object for a profile_pic key
    if "profile_pic" not in request.files:
        flash("No profile_pic key in request.files", "danger")
        return redirect("/")

    # if key is in object, save it in a variable called file
    file = request.files["profile_pic"]

    #  check if filename attribute on the object and if empty, means user submit empty form, so return error
    if file.filename == "":
        flash("Please select a file", "danger")
        return redirect("/")

    # check that there is a file and that it has an allowed filetype
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        profile_pic_update = User.update(profile_pic=file.filename).where(User.id==id).execute()
        flash("Profile picture successfully updated", "success")
        return render_template('users/edit.html')
    else:
        flash("Please try again", "danger")
        return redirect("/")

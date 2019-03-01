from app import app
from flask import Flask, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from models.image import Image
from flask_login import current_user
from werkzeug.utils import secure_filename
from instagram_web.util.s3_helpers import upload_file_to_s3, allowed_file


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')

@images_blueprint.route('/', methods=['POST'])
def create():
    # check request.files object for a image key
    if "image_post" not in request.files:
        flash("No image key in request.files", "danger")
        return redirect( url_for('users.show', username=current_user.name) )

    # if key is in object, save it in a variable called file
    file = request.files["image_post"]

    #  check if filename attribute on the object and if empty, means user submit empty form, so return error
    if file.filename == "":
        flash("Please select a file", "danger")
        return redirect( url_for('users.show', username=current_user.name) )

    # check that there is a file and that it has an allowed filetype
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        Image.create(image=file.filename, user=current_user.id)
        flash("Post successfully uploaded", "success")
        return redirect( url_for('users.show', username=current_user.name) )
    else:
        flash("Please try again", "danger")
        return redirect( url_for('users.show', username=current_user.name) )
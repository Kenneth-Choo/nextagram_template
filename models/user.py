from app import app
from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property


class User(UserMixin,BaseModel):
    name = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    profile_pic = pw.CharField(unique=False, null=True)

    def validate(self):
        duplicate_name = User.get_or_none(User.name == self.name)
        duplicate_emails = User.get_or_none(User.email == self.email)

        if duplicate_emails:
            self.errors.append('User email not unique')
        
    @hybrid_property
    def profile_image_url(self):
        if not self.profile_pic:
            return "//placehold.it/200"
        else:
            return app.config['S3_DOMAIN'] + self.profile_pic
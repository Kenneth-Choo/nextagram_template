from app import app
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image = pw.CharField()

    @hybrid_property
    def user_image_url(self):
        return app.config['S3_DOMAIN'] + self.image

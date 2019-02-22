from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    name = pw.CharField(unique=True, null=False)
    email = pw.TextField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)


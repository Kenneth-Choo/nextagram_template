from app import app
from models.base_model import BaseModel
from models.image import Image
import peewee as pw

class Donation(BaseModel):
    image = pw.ForeignKeyField(Image, backref='donations')
    receiver_id = pw.IntegerField()
    sender_id = pw.IntegerField()
    amount = pw.DecimalField()
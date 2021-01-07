from datetime import datetime
from marshmallow import *
from service import db

class LogImageRecognition(db.Model):
    __tablename__ = 'tl_image_recognition'
    AUTOMATION_ID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    TOTAL_DATA    = db.Column()
    TOTAL_VALID   = db.Column()
    TOTAL_SKIPPED = db.Column()
    FINISHED      = db.Column()
    CREATED_AT    = db.Column(default=datetime.now())
    CREATED_BY    = db.Column()
    UPDATED_AT    = db.Column(onupdate=datetime.now)
    UPDATED_BY    = db.Column()

from datetime import datetime
from marshmallow import *
from service import db

class GmToken(db.Model):
    __tablename__ = 'tm_gm_token'
    EMAIL         = db.Column(db.String(), primary_key = True)
    TOKEN         = db.Column(db.String())
    CREATED_AT    = db.Column(db.DateTime, default=datetime.now())
    CREATED_BY    = db.Column(db.String())
    UPDATED_AT    = db.Column(db.DateTime, onupdate=datetime.now)
    UPDATED_BY    = db.Column(db.String())
    DELETE_AT     = db.Column(db.DateTime)
    DELETE_BY     = db.Column(db.String())
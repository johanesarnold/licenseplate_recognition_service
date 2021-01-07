from datetime import datetime
from marshmallow import *
from service import db

class BookingVhcImage(db.Model):
    __tablename__ = 'tr_booking_vhc_image'
    VHC_IMAGE_ID   = db.Column(db.String(), primary_key=True)
    BOOKING_ID    = db.Column(db.String())
    IMC_ID        = db.Column(db.String())
    VHC_IMAGE     = db.Column(db.String())
    CREATED_AT    = db.Column(db.DateTime, default=datetime.now())
    CREATED_BY    = db.Column(db.String())
    UPDATED_AT    = db.Column(db.DateTime, onupdate=datetime.now)
    UPDATED_BY    = db.Column(db.String())
    DELETE_AT     = db.Column(db.DateTime)
    DELETE_BY     = db.Column(db.String())

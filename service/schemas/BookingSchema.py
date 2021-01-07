from marshmallow_sqlalchemy  import ModelSchema
from service.models.Booking import *

class BookingSchema(ModelSchema):
    class Meta:
        model = Booking
        ordered = True
bookingAllSchema = BookingSchema(many=True)
bookingOneSchema = BookingSchema()
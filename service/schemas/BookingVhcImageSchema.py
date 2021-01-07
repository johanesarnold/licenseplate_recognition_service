from marshmallow_sqlalchemy  import ModelSchema
from service.models.BookingVhcImage import *

class BookingVhcImageSchema(ModelSchema):
    class Meta:
        model = BookingVhcImage
        ordered = True
bookingVhcImageAllSchema = BookingVhcImageSchema(many=True)
bookingVhcImageOneSchema = BookingVhcImageSchema()
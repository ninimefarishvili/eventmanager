
from ninja import Schema, Field, ModelSchema
from .models import Stadium, Event

class StadiumSchema(Schema):
    name: str
    address: str
    capacity: int

    class Meta:
        model = Stadium
        exclude = ["id"]

class EventSchema(ModelSchema):
    name: str
    stadium: StadiumSchema
    is_active: bool

    class Meta:
        model = Event
        exclude = ["date"]
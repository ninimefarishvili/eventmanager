
from ninja import Schema, Field, ModelSchema
from .models import Stadium, Event ,Ticket, OrganizerCompany

class StadiumSchema(Schema):
    name: str
    address: str
    capacity: int

    class Meta:
        model = Stadium
        exclude = ["id"]

class EventSchema(Schema):
    name: str
    stadium: StadiumSchema
    is_active: bool

    class Meta:
        model = Event
        exclude = ["id"]


class TicketSchema(ModelSchema):
    customer : str
    event : EventSchema
    bougtht_at : str

    class Meta:
        model = Ticket
        exclude = ["id"]

class OrganizerCompanySchema(ModelSchema):
    name:str
    address :  str
    events_organized : EventSchema

    class Meta:
        model = OrganizerCompany
        exclude = ['id']    

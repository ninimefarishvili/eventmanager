from ninja import Router

from .models import Customer, Stadium, Event, Ticket, OrganizerCompany
from .schema import StadiumSchema, EventSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Stadium


router = Router()


@router.get("/events")
def get_events(request):
    events = Event.objects.all()
    return {"events": [event.tojson() for event in events]}

@router.get("/event-ticket-count/{event_id}")
def get_event_ticket_count(request, event_id: int):
    result = Event.events_with_ticket_count(event_id)
    return result

@router.get("/tickets")
def get_tickets(request, customer_id=None, date_from=None):

    qs = Ticket.objects.all()

    if customer_id:
        qs = qs.filter(customer__id=customer_id)

    if date_from:
        qs = qs.filter(bought_at__gt=date_from)
    
    return [q.tojson() for q in qs]


@router.get("/events-filtered")
def get_filtered_events(request, month = None):
    events = Event.objects.all()

    if month:
        events = Event.filter(date__month = month)

    return [event.tojson() for event in events]
    


@router.get("/stadiums")
def get_stadiums(request, capacity: int = None):
    stadiums = Stadium.objects.all()

    if capacity:
        stadiums = stadiums.filter(capacity__gt=capacity)
    
    return [StadiumSchema.from_orm(stadium) for stadium in stadiums]




class StadiumList(APIView):
    def get(self, request, format=None):
        stadiums = Stadium.objects.all
        return Response(stadiums)

@router.get("/events")
def get_events(request, date_from = None, stadium_name = None):
    events = Event.objects.filter(is_active=True).select_related("stadium")

    if date_from:
        events = events.filter(date__gt=date_from)
    
    if stadium_name:
        events = events.filter(stadium__name=stadium_name)
    
    return {
        "result": [
            event.tojson() for event in events
        ]
    }

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F, Avg,Count
from django.db.models.functions import TruncMonth


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=False)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    def tojson(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "email": self.email,
        }

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"


class Stadium(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def tojson(self):
        return {
            "name": self.name,
            "address": self.address,
            "capacity": self.capacity
        }

    @staticmethod
    def events_in_large_stadiums(min_capacity):
    
        return Stadium.objects.filter(capacity__gt=min_capacity)

    @staticmethod
    def average_capacity_of_stadiums():
        """
        Calculate the average capacity of all stadiums.
        """
        return Stadium.objects.aggregate(Avg("capacity"))

    @staticmethod
    def stadiums_with_high_or_low_capacity(threshold):
        """
        Retrieve stadiums with either very high or very low capacity.
        """
        pass
    @staticmethod
    def stadium_capacity_difference(threshold):
        """
        Retrieve stadiums where the capacity exceeds or falls short of the given threshold.
        """
        return Stadium.objects.filter(Q(capacity__gt=threshold) | Q(capacity__lt=threshold))
    
class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="events")
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name
    
    def tojson(self):
        return {
            "name": self.name,
            "date": self.date,
            "stadium": self.stadium.tojson() if self.stadium else None,
            "is_active": self.is_active,
        }

    @staticmethod
    def events_with_stadium_details():
        """
        Retrieve all events with their associated stadium details.
        """
        return Event.objects.select_related("Stadium").all()

    @staticmethod
    def events_with_ticket_count():
        """
        Retrieve events with the number of tickets sold for each event.
        """
        return Event.objects.annotate(Ticket_count = Count(Ticket)).all()

    @staticmethod
    def active_events_by_month():
        """
        Count active events grouped by the month of their date.
        """
        return Event.objects.filter(is_active=True).annotate(month=TruncMonth('date')).values('month').annotate(event_count=Count('id')).order_by('month')


    @staticmethod
    def events_on_specific_days(start_date, end_date):
        """
        Retrieve events scheduled within a specific date range or on a certain day.
        """
        return Event.objects.filter(date__range=[start_date, end_date])

    @staticmethod
    def events_with_large_attendance_and_active(threshold):
        """
        Retrieve active events with a minimum attendance threshold.
        """
        return Event.objects.filter(is_active=True).annotate(ticket_count=Count('ticket')).filter(ticket_count__gte=threshold)


class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    def tojson(self):
        return {
            "customer": self.customer.tojson(),
            "customer_id": self.customer.id,
            "bought_at": self.bought_at,
        }

    @staticmethod
    def tickets_with_customer_and_event():
        """
        Retrieve tickets with their related customer and event data.
        """
        return Ticket.objects.select_related("customer", "event").all()

    @staticmethod
    def tickets_for_customer(customer_id):
        """
        Retrieve tickets for a specific customer with event details.
        """
        return Ticket.objects.filter(customer__id=customer_id).select_related("event")

    @staticmethod
    def total_tickets_sold():
        """
        Calculate the total number of tickets sold.
        """
        return Ticket.objects.count()


    @staticmethod
    def tickets_per_event():
        """
        Retrieve the number of tickets sold for each event.
        """
        pass

    @staticmethod
    def tickets_in_date_range_or_customer(date_range, customer_id):
        """
        Retrieve tickets sold within a date range or for a specific customer.
        """
        return Ticket.objects.filter(Q(bought_at__range=date_range) | Q(customer_id=customer_id))

    @staticmethod
    def tickets_older_than_year():
        """
        Retrieve tickets purchased more than a year ago.
        """
        one_year_ago = timezone.now() - timedelta(days=365)
        return Ticket.objects.filter(bought_at__lt=one_year_ago)

    @staticmethod
    def ticket_bought_recently_with_field_comparison():
        """
        Retrieve tickets where the bought_at field matches a certain condition with another field.
        """
        return Ticket.objects.filter(bought_at__gte=F('event__date'))


class OrganizerCompany(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=50, null=True, blank=True)
    events_organized = models.ManyToManyField(Event, related_name="companies")

    def __str__(self):
        return self.name

    @staticmethod
    def companies_with_events():
        """
        Retrieve organizer companies with the events they organize.
        """
        return OrganizerCompany.objects.prefetch_related('events_organized').all()


    @staticmethod
    def companies_for_event(event_id):
        """
        Retrieve companies organizing a specific event.
        """
        return OrganizerCompany.objects.filter(events_organized__id=event_id)

    @staticmethod
    def company_event_count():
        """
        Retrieve companies with the count of events they have organized.
        """
        return OrganizerCompany.objects.annotate(event_count=Count('events_organized')).all()


    @staticmethod
    def average_events_per_company():
        """
        Calculate the average number of events organized per company.
        """
        return OrganizerCompany.objects.aggregate(Avg('events_organized__count'))

    @staticmethod
    def companies_with_events_in_large_stadiums_or_high_capacity(min_capacity):
        """
        Retrieve companies organizing events in large stadiums or with high capacity events.
        """
        return OrganizerCompany.objects.filter(
        Q(events_organized__stadium__capacity__gt=min_capacity)
    ).distinct()

    @staticmethod
    def company_event_relationship_based_on_date():
        """
        Retrieve companies with events scheduled after a specific date and address matching criteria.
        """
        return OrganizerCompany.objects.filter(events_organized__date__gt=date)

    @staticmethod
    def companies_with_address_as_event_attribute():
        """
        Retrieve companies where the address matches an attribute of their events.
        """
        return OrganizerCompany.objects.filter(address=F('events_organized__stadium__address'))


    class Meta:
        verbose_name = "ორგანიზატორი კომპანია"
        verbose_name_plural = "ორგანიზატორი კომპანიები"

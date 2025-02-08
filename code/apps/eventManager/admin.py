from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Stadium, Event, Ticket, Customer, OrganizerCompany

@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')
    list_filter = ('capacity',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'stadium', 'is_active')
    list_filter = ('stadium', 'date', 'is_active')
    search_fields = ('name',)
    date_hierarchy = 'date'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'event', 'bought_at')
    list_filter = ('event', 'bought_at')
    search_fields = ('customer__username', 'event__name')
    date_hierarchy = 'bought_at'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(OrganizerCompany)
class OrganizerCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    filter_horizontal = ("events_organized",)
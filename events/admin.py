from django.contrib import admin
from .models import Event, OrderTickets, EventTickets, Ticket
# Register your models here.

@admin.register(EventTickets)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'price', 'number']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'price', 'quantity', 'user']

class TicketInLine(admin.TabularInline):
    model = EventTickets
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['categories','name','desc', 'date']

    inlines = [TicketInLine]
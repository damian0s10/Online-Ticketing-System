from django.contrib import admin
from .models import Event, PurchasedTickets, TicketType
# Register your models here.

@admin.register(TicketType)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'price', 'count']

class TicketInLine(admin.TabularInline):
    model = TicketType
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['categories','name','desc', 'date']

    inlines = [TicketInLine]
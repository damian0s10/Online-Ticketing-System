from django.contrib import admin
from .models import Event, OrderTickets, EventTickets, Ticket, OrderTickets
# Register your models here.

@admin.register(EventTickets)
class EventTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_type', 'price', 'number')



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'event_ticket', 'order')
    

class TicketInLine(admin.TabularInline):
    model = EventTickets
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('categories','name','desc', 'date')
    inlines = [TicketInLine]



class PurchasedTicketInLine(admin.TabularInline):
    model = Ticket
    extra = 0

@admin.register(OrderTickets)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'paid')
    inlines = [PurchasedTicketInLine]
    
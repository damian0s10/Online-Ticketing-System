from django.contrib import admin
from .models import Event, OrderTickets, EventTickets, Ticket, OrderTickets
from django.utils.safestring import mark_safe
from django.urls import reverse

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

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('events:admin_order_view', args=[obj.id])))
order_pdf.short_desciption = 'Tickets' 

@admin.register(OrderTickets)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'paid', order_pdf)
    inlines = [PurchasedTicketInLine]
    
    
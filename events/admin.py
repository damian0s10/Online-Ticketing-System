from django.contrib import admin
from .models import Event, OrderTickets, EventTickets, Ticket, OrderTickets
from django.utils.safestring import mark_safe
from django.urls import reverse
import csv
import datetime
from django.http import HttpResponse

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

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('events:admin_order_view', args=[obj.id])))
order_pdf.short_desciption = 'Tickets' 

@admin.register(OrderTickets)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'paid', 'created', 'included', order_pdf)
    inlines = [PurchasedTicketInLine]
    actions = [export_to_csv]
    
    
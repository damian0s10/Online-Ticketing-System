from celery import task
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import get_object_or_404
from .models import OrderTickets, EventTickets
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from django.conf import settings

@task
def send_order_confirmation(order_id):
    order = get_object_or_404(OrderTickets, id=order_id)
    subject = 'Order confirmation'
    message = 'Hi {}.Your order number {} has been created. Make a payment and then you will receive a ticket.'.format(order.user.first_name, order_id)
    address_email = 'onlinetickets56@gmail.com'
    send_mail(subject,message, address_email, [order.user.email])

@task
def send_tickets(order_id):
    order = get_object_or_404(OrderTickets, id=order_id)
    subject = 'Ticket'
    message = 'Hi {}. Your payment has been approved. Your ticket is attached below.'.format(order.user.first_name)
    address_email = 'onlinetickets56@gmail.com'

    email = EmailMessage(subject,
                        message,
                        address_email,
                        [order.user.email])

    # Generate PDF
    html = render_to_string('admin/order/ticket_pdf.html', 
                            {'order':order,
                            'tickets':order.order.all()})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out, 
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'pdf.css'
        )])

    # Attaching PDF
    email.attach('order_{}.pdf'.format(order.id),
                 out.getvalue(),
                 'application/pdf')

    # Send e-mail
    email.send()

@task
def include_unfinished_payment(order_id):
    order = get_object_or_404(OrderTickets, id = order_id)
    if not order.included:
        for ticket in order.order.all():
            event_ticket = get_object_or_404(EventTickets, id=ticket.event_ticket.id)
            event_ticket.number += ticket.quantity
            event_ticket.save()
        order.included = True
        order.save()
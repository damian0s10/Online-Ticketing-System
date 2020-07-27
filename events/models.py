from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    CHOICES = (
        ('sport', 'sport'),
        ('concerts', 'concerts'),
        ('thearte', 'thearte'),
        ('stand-up', 'stand-up'),
        ('for-children', 'for-children'),
        ('cinema', 'cinema'),
        ('others', 'others'),
    )
    categories = models.CharField(max_length=20, choices=CHOICES)
    name = models.CharField(max_length=300)
    desc = models.TextField()
    date = models.DateTimeField()
    image = models.FileField(upload_to='images')

class EventTickets(models.Model):
    ticket_type = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number = models.PositiveIntegerField()
    event = models.ForeignKey(Event, related_name='event_tickets', on_delete=models.CASCADE)

class OrderTickets(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    braintree_id = models.CharField(max_length=150, blank=True)
    paid = models.BooleanField(default=False) 
    
class Ticket(models.Model):
    quantity = models.PositiveIntegerField()
    event_ticket = models.ForeignKey(EventTickets, related_name='tickets', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderTickets, related_name='order', on_delete=models.CASCADE)
    


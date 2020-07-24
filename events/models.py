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

class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)

class OrderTickets(models.Model):
    tickets = models.ManyToManyField(Ticket, related_name="order_tickets", blank=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


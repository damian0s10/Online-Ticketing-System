from django.db import models

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


class TicketType(models.Model):
    ticket_type = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.PositiveIntegerField()
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)


class PurchasedTickets(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    tickets = models.ManyToManyField(TicketType, related_name="purchased_tickets", blank=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


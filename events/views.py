from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .models import Event, EventTickets, Ticket, OrderTickets
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .forms import UserCreateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .tasks import send_order_confirmation, include_unfinished_payment
import weasyprint
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta
from .documents import EventDocument
from django.utils import timezone
import redis

r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB)

class UserRegistrationView(CreateView):
    template_name='registration/registration.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('dashboard')
   
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result

class Dashboard(TemplateResponseMixin, View):
    template_name = 'dashboard.html'

    def get(self, request):
        query = request.GET.get('search')
        event_most_viewed = None
        events = None
        if query:
            events = EventDocument.search().query("match", name=query).to_queryset().filter(date__gte=timezone.now())
            
        else:
            # Get a dictionary of the most displayed events
            event_ranking = r.zrange('event_ranking', 0, -1, desc=True)
            print(event_ranking)

            # Get the most displayed events
            event_ids = [int(id) for id in event_ranking]
            event_most_viewed = list(Event.objects.filter(date__gte=timezone.now()).filter(id__in=event_ids))[:6]
            print(event_most_viewed)
            event_most_viewed.sort(key=lambda x: event_ids.index(x.id))
            print(event_most_viewed)
        return self.render_to_response({'search':events,
                                        'most_viewed':event_most_viewed,
                                        })

class EventListView(TemplateResponseMixin, View):
    template_name = 'events/list.html'
    
    def get(self, request, event):
        
        events = Event.objects.filter(categories=event).filter(date__gte=timezone.now())
        
        return self.render_to_response({'events': events})

class EventDetailView(TemplateResponseMixin, View):
    template_name = 'events/detail.html'
    event = None
    order = None

    def calculate_price(self):
        total_price = 0

        for ticket in self.order.order.all():
            total_price += ticket.quantity * ticket.event_ticket.price
        
        self.order.total_price = total_price
        self.order.save()

    def dispatch(self, request, pk):
        self.event = get_object_or_404(Event, id=pk)
        return super().dispatch(request,pk)

    def get(self, request, pk):
        if self.event.date > timezone.now():
            
            total_views = r.incr('event:{}:views'.format(self.event.id))
            r.zincrby('event_ranking', 1, self.event.id)
            context = {'event': self.event,
                       'tickets': self.event.event_tickets.all().order_by('price'),
                       'total_views': total_views
                        }
            return self.render_to_response(context)
        else:
            return redirect(reverse('events:dashboard'))

    def post(self, request, pk):
        if request.user.is_authenticated:
            tickets = []

            # Create an order
            self.order = OrderTickets(user=request.user)
            self.order.save()

            
            # Adding tickets to the order
            for key, value in request.POST.items(): 
                
                if key != 'csrfmiddlewaretoken' and value:
                    event_ticket = get_object_or_404(EventTickets, id=key)
                    if int(value) <= event_ticket.number:
                        t = Ticket(quantity=value,
                                event_ticket=event_ticket,
                                order=self.order)
                        t.save()
                        event_ticket.number -= int(value)
                        event_ticket.save()
                        tickets.append(t)
                    else: 
                        self.order.delete()
                        return self.render_to_response({'event': self.event,
                                            'tickets': self.event.event_tickets.all().order_by('price'),
                                            'inaccessible': True })
            if tickets:
                self.calculate_price()
                request.session['order_id'] = self.order.id
                
                # Sending an email confirming the order
                send_order_confirmation.delay(self.order.id)

                # Checking whether the not successful payment the number of tickets has been refunded 
                
                include_unfinished_payment.apply_async(args=[self.order.id], countdown=300)

                return redirect(reverse('payment:process'))
            
            return self.render_to_response({'event': self.event,
                                        'tickets': self.event.event_tickets.all().order_by('price'),
                                        'inaccessible': True})

        return self.render_to_response({'event': self.event,
                                        'tickets': self.event.event_tickets.all().order_by('price'),
                                        'not_authenticaded': True})




@staff_member_required
def admin_order_view(request, order_id):
    order = get_object_or_404(OrderTickets, id=order_id)
    html = render_to_string('admin/order/ticket_pdf.html', 
                            {'order':order,
                             'tickets':order.order.all()})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, 
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'pdf.css'
        )])
    return response
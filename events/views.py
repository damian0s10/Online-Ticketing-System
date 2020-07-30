from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .models import Event, EventTickets, Ticket, OrderTickets
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .forms import UserCreateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .tasks import send_order_confirmation
import weasyprint
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

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
        return self.render_to_response({})

class EventListView(TemplateResponseMixin, View):
    template_name = 'events/list.html'
    
    def get(self, request, event):
        events = Event.objects.filter(categories=event)
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
        
        return self.render_to_response({'event': self.event,
                                        'tickets': self.event.event_tickets.all().order_by('price') })
    
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
            
                return redirect(reverse('payment:process'))
            
            return self.render_to_response({'event': self.event,
                                        'tickets': self.event.event_tickets.all().order_by('price'),
                                        'inaccessible': True})

        return self.render_to_response({'event': self.event,
                                        'tickets': self.event.event_tickets.all().order_by('price'),
                                        'not_authenticaded': True})



# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(OrderTickets, id=order_id)
#     return render(request,
#                 'admin/order/detail.html',
#                 {'order': order})

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
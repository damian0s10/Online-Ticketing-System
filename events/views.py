from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .models import Event
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .forms import UserCreateForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

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

    def dispatch(self, request, pk):
        self.event = get_object_or_404(Event, id=pk)
        return super().dispatch(request,pk)

    def get(self, request, pk):
        return self.render_to_response({'event': self.event,
                                        'tickets': self.event.tickets.all() })
    
    #def post(self, request, pk):

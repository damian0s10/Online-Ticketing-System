from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from .models import Event
from django.views.generic.list import ListView

class Dashboard(TemplateResponseMixin, View):
    template_name = 'base.html'

    def get(self, request):
        
        return self.render_to_response({})

class EventListView(TemplateResponseMixin, View):
    template_name = 'events/list.html'

    def get(self, request, event):
        events = Event.objects.filter(categories=event)
        return self.render_to_response({'events': events})
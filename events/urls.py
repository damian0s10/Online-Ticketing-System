from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.Dashboard.as_view(),
         name='dashboard'),
    path('<event>/',
         views.EventListView.as_view(),
         name='event_list_view'),
]
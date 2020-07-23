from django.urls import path
from . import views

urlpatterns = [
     path('',
         views.Dashboard.as_view(),
         name='dashboard'),
     path('register/',
        views.UserRegistrationView.as_view(),
        name='user_registration'),
     path('<event>/',
         views.EventListView.as_view(),
         name='event_list_view'),
     path('event/<pk>',
          views.EventDetailView.as_view(),
          name='event_detail_view'),
]

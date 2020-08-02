from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('',
        views.Dashboard.as_view(),
        name='dashboard'),
    path('register/',
        views.UserRegistrationView.as_view(),
        name='user_registration'),
    path('profile/',
        views.ProfileView.as_view(),
        name='profile_view'),
        path('profile/update/',
        views.ProfileUpdateView.as_view(),
        name='profile_update'),
    path('profile/password/',
        views.ChangePasswordView.as_view(),
        name='change_password'),
    path('profile/tickets/',
        views.UserTicketsView.as_view(),
        name='user_tickets'),
    path('profile/tickets/download/<int:order_id>/',
        views.download_ticket,
        name='download_ticket'),
    path('<event>/',
        views.EventListView.as_view(),
        name='event_list_view'),
    path('event/<pk>/',
        views.EventDetailView.as_view(),
        name='event_detail_view'),
    path('admin/events/ordertickets/<int:order_id>/pdf/',
        views.admin_order_view,
        name='admin_order_view'),
    
]

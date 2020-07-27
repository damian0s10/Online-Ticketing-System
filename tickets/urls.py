from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('admin/', admin.site.urls),
     path('events/', include('events.urls')),
     path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), 
         name='login'),
     path('logout/', auth_views.LogoutView.as_view(), 
         name='logout'),
     path('payment/', include('payment.urls', namespace='payment')),
     path('',
         views.Dashboard.as_view(),
         name='dashboard'),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
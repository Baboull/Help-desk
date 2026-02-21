from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register_view, name='register'),
    path('', include('django.contrib.auth.urls')),  
    path('tickets/', include('tickets.urls')),
    path('account/', include('users.urls')),
    path('', core_views.home_redirect, name='home'),
]

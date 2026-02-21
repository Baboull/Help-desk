from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_settings, name='profile_settings'),
]

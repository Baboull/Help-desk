from django.urls import path
from . import views

urlpatterns = [
    path('my-tickets/', views.client_dashboard, name='client_dashboard'),
    path('queue/', views.staff_dashboard, name='staff_dashboard'),
    path('new/', views.ticket_create, name='ticket_create'),
    path('resolved/', views.resolved_tickets, name='resolved_tickets'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]

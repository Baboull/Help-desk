from django.contrib import admin
from .models import Ticket, InternalNote

admin.site.register(Ticket)
admin.site.register(InternalNote)

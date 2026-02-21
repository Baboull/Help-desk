from django import forms
from .models import Ticket
from chat.models import Message

class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }
        labels = {
            'content': ''
        }

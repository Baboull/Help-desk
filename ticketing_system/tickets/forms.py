from django import forms
from .models import Ticket
from chat.models import Message
from users.models import User

class TicketCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(role__in=['staff', 'admin'])
        self.fields['assigned_to'].label = "Assign to specific agent (optional)"

    class Meta:
        model = Ticket
        fields = ['title', 'department', 'assigned_to', 'description']
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

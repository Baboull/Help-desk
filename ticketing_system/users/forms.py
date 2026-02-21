from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('client', 'Client'), ('staff', 'Staff')], required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CustomPasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label='Current Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password',
                                   help_text=password_validation.password_validators_help_text_html())
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        cp = self.cleaned_data.get('current_password')
        if not self.user.check_password(cp):
            raise forms.ValidationError('Current password is incorrect.')
        return cp

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        if p1:
            password_validation.validate_password(p1, self.user)
        return cleaned

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailLoginForm(AuthenticationForm):
    # Show "Email" instead of "Username" on the login form (just changing the label)
    username= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

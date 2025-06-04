from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class EmailLoginForm(AuthenticationForm):
    # Show "Email" instead of "Username" on the login form (just changing the label)
    username= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

class EmailSignupForm(UserCreationForm):
    username= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
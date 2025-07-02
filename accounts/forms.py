from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailLoginForm(AuthenticationForm):
    # Show "Email" instead of "Username" on the login form (just changing the label)
    username= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

class EmailSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    username= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    def save(self, commit=True):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(email=email, password=password)
        return user

class NicknameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname']
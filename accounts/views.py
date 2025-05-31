from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

from django.template.response import TemplateResponse
from django.contrib.auth.views import PasswordResetCompleteView

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        response = TemplateResponse(
            request,
            self.template_name,
            context=self.get_context_data()
        )
        print(f"Resolved template: {response.template_name}")  # Log the resolved template
        return response
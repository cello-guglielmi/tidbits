from .forms import EmailSignupForm, NicknameForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = EmailSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

'''
class UserDetail(DetailView):
    model = User
    template_name = 'user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
'''

@login_required
def userProfile(request):
    return render(request, 'accounts/user_profile.html', {'user': request.user})

@login_required
def updateNickname(request):
    user = request.user
    if request.method == 'POST':
        form = NicknameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/components/nickname-view.html')
        else:
            return render(request, 'accounts/components/nickname-edit.html', {'form': form})
    # elif request.method == 'GET':
    edit_toggle = request.GET.get('edit')
    if edit_toggle:
        form = NicknameForm(instance=user)
        return render(request, 'accounts/components/nickname-edit.html', {'form': form})
    # elif not edit_toggle:
    return render(request, 'accounts/components/nickname-view.html')
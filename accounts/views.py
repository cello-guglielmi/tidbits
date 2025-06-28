from .forms import EmailSignupForm, NicknameForm
from django.shortcuts import render, redirect
from .decorators import active_login_required
from django.conf import settings
from django.contrib.auth import get_user_model, logout
from quotes.models import QuoteSubmission
User = get_user_model()

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

@active_login_required
def userProfile(request):
    return render(request, 'accounts/user_profile.html', {'user': request.user})

@active_login_required
def closeAccount(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return redirect(settings.LOGIN_URL)
    return render(request, 'accounts/account_delete_confirm.html')


@active_login_required
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
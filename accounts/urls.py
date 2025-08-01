from django.urls import path, include
from . import views
from .forms import EmailLoginForm
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile', views.userProfile, name='user_profile'),
    path('close_account', views.closeAccount, name='close_account'),
    path('update_nickname/', views.updateNickname, name='update_nickname'),
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(authentication_form=EmailLoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), # PW reset request
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), # PW reset email sent
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # PW confirm email token
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), # PW reset complete
]
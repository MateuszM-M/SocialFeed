from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
from .forms import *

app_name = 'Accounts'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        form_class=UserLoginForm,
        redirect_authenticated_user=True),
         name='login'),

     path('login-without-credentials/',
          views.login_without_credentials,
          name='login_without_credentials'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        form_class=UserChangePasswordForm,
        success_url=reverse_lazy('Accounts:password_change_done')),
         name='password_change'),

    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('Accounts:password_reset_done')),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('Accounts:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('register/', views.register, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('u/<username>', views.profile_view, name='profile_view'),

    path('invite/<username>', views.invite, name='invite'),
    path('accept/', views.accept, name='accept'),
    path('reject/', views.reject, name='reject'),
    path('delete_friend/<username>', views.delete_friend, name='delete_friend'),
    path('friends/<username>', views.users_friends, name='user_friends'),
    path('search/', views.profile_search, name='search'),
    path('users/', views.recommended_users, name='users'),
]

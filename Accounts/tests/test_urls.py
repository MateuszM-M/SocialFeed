from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from Accounts.views import *

class TestUrls(SimpleTestCase):

    def test_login_url_resolving(self):
        url = reverse('Accounts:login')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.LoginView)

    def test_logout_url_resolving(self):
        url = reverse('Accounts:logout')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.LogoutView)

    def test_dashboard_url_resolving(self):
        url = reverse('Accounts:dashboard')
        self.assertEquals(
            resolve(url).func,
            dashboard)

    def test_password_change_url_resolving(self):
        url = reverse('Accounts:password_change')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordChangeView)

    def test_password_change_done_url_resolving(self):
        url = reverse('Accounts:password_change_done')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordChangeDoneView)

    def test_password_reset_resolving(self):
        url = reverse('Accounts:password_reset')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetView)

    def test_password_reset_done_resolving(self):
        url = reverse('Accounts:password_reset_done')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetDoneView)

    def test_password_reset_complete_resolving(self):
        url = reverse('Accounts:password_reset_complete')
        self.assertEquals(
            resolve(url).func.view_class,
            auth_views.PasswordResetCompleteView)

    def test_register_resolving(self):
        url = reverse('Accounts:register')
        self.assertEquals(
            resolve(url).func,
            register)

    def test_edit_profile_resolving(self):
        url = reverse('Accounts:edit_profile')
        self.assertEquals(
            resolve(url).func,
            edit_profile)

    def test_profile_view_resolving(self):
        url = reverse('Accounts:profile_view', args=['some_name'])
        self.assertEquals(
            resolve(url).func,
            profile_view)

    def test_accept_view_resolving(self):
        url = reverse('Accounts:accept')
        self.assertEquals(
            resolve(url).func,
            accept)

    def test_reject_view_resolving(self):
        url = reverse('Accounts:reject')
        self.assertEquals(
            resolve(url).func,
            reject)

    def test_delete_friend_view_resolving(self):
        url = reverse('Accounts:delete_friend', args=['some_name'])
        self.assertEquals(
            resolve(url).func,
            delete_friend)

    def test_friends_view_resolving(self):
        url = reverse('Accounts:user_friends', args=['some_name'])
        self.assertEquals(
            resolve(url).func,
            users_friends)

    def test_search_view_resolving(self):
        url = reverse('Accounts:search')
        self.assertEquals(
            resolve(url).func,
            profile_search)

    def test_recommended_users_resolving(self):
        url = reverse('Accounts:users')
        self.assertEquals(
            resolve(url).func,
            recommended_users)

































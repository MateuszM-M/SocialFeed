from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from Accounts.models import Profile, Contact
from Accounts.views import accept
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(
            username='my_nickname',
            email='name@invalid.com',
        )
        self.user1.set_password("my_paSW1")
        self.user1.save()
        self.profile1 = Profile.objects.create(
            user=self.user1,
            firstname='first',
            lastname='last',
        )

        self.user2 = User.objects.create(
            username='my_nickname2',
            email='name@invalid.com',
        )
        self.user2.set_password("my_paSW2")
        self.user2.save()
        self.profile2 = Profile.objects.create(
            user=self.user2,
            firstname='firstname',
            lastname='lastname',
        )

    def test_dashboard_as_logged_out(self):
        dashboard = reverse('Accounts:dashboard')

        response = self.client.get(dashboard)
        self.assertEquals(response.status_code, 302)

        response = self.client.get(dashboard, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_dashboard_as_logged_in(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')


        dashboard = reverse('Accounts:dashboard')

        response = self.client.get(dashboard, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/dashboard.html')

    def test_register_view(self):
        url = reverse('Accounts:register')
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/register.html')

    def test_valid_form_register_view(self):
        url = reverse('Accounts:register')
        response = self.client.post(
            url, {
                'username': 'my_name',
                'email': 'my_name@valid.com',
                'password': 'my_paSW8',
                'password2': 'my_paSW8',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/edit_profile.html')
        self.assertEquals(User.objects.all().count(), 3)

    def test_not_same_password_register_view(self):
        url = reverse('Accounts:register')
        response = self.client.post(
            url, {
                'username': 'my_name',
                'email': 'my_name@valid.com',
                'password': 'my_paSW8',
                'password2': 'my_paSW8432',
            },
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/register.html')
        self.assertEquals(User.objects.all().count(), 2)

    def test_valid_form_edit_profile(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')

        url = reverse('Accounts:edit_profile')
        response = self.client.post(
            url, {
                'firstname': 'Jane',
                'lastname': 'Doe',
            },
            follow=True
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/edit_profile.html')
        self.assertTrue(Profile.objects.filter(lastname='Doe'))

    def test_profile_view(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')

        url = reverse('Accounts:profile_view', args=[self.user1])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/view_profile.html')


    def test_invite_friend(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        url = reverse('Accounts:invite', args=[self.user2])
        response = self.client.post(url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Contact.objects.all().count(), 1)

    def test_recommended_users(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        url = reverse('Accounts:users')
        response = self.client.post(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/people.html')

    def test_users_friends(self):
        self.client.login(username=self.user1.username,
                          password='my_paSW1')
        url = reverse('Accounts:user_friends', args=[self.user1])
        response = self.client.post(url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/friend_list.html')


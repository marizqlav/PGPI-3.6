from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile
from store.models import Customer

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(
            user=self.user,
            name=self.user.username,
            email=self.user.email
        )
        self.profile, created = Profile.objects.get_or_create(user=self.user)

    def test_home_GET(self):
        response = self.client.get(reverse('users-home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_register_POST(self):
        response = self.client.post(reverse('users-register'), {
            'first_name': 'Test',
            'last_name': 'User2',
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user_model.objects.count(), 2)


    def test_profile_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('users-profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_POST(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('users-profile'), {
            'username': 'updatedusername',
            'email': 'updatedemail@example.com',
            'avatar': '',
            'bio': 'This is a test bio',
        })

        self.assertEquals(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEquals(self.user.username, 'updatedusername')
        self.assertEquals(self.user.email, 'updatedemail@example.com')

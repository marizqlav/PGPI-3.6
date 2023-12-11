from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Claim

class ClaimTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.claim = Claim.objects.create(user=self.user, title='Test Claim', description='This is a test claim.')

    def test_claim_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('claim_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Claim')

    def test_claim_detail(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('claim_detail', args=(self.claim.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Claim')

    def test_claim_create(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('claim_create'), {'title': 'New Claim', 'description': 'This is a new claim.'})
        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.assertEqual(Claim.objects.count(), 2)

    def test_claim_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('claim_update', args=(self.claim.id,)), {'title': 'Updated Claim', 'description': 'This is an updated claim.'})
        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.claim.refresh_from_db()
        self.assertEqual(self.claim.title, 'Updated Claim')

    def test_claim_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('claim_delete', args=(self.claim.id,)))
        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.assertEqual(Claim.objects.count(), 0)

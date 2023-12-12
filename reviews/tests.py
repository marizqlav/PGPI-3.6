from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from store.models import Customer  # Importa el modelo Customer

class ReviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')  # Crea un objeto Customer
        self.review = Review.objects.create(user=self.user, title='Test Review', content='This is a test review.')

    
    def test_add_review(self):
        # Create a new user that has not created a review before
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.customer = Customer.objects.create(user=new_user, name='New Customer', email='new@example.com')
        self.client.login(username='newuser', password='12345')
        response = self.client.post(reverse('add_review'), {'title': 'New Review', 'content': 'This is a new review.', 'rating': '5'})
        self.assertEqual(response.status_code, 302)  # Redirection to 'review_list'
        self.assertTrue(Review.objects.filter(user=new_user, title='New Review').exists(), "New Review does not exist")

    def test_review_list(self):
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Review')

    def test_edit_review(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_review', args=[self.review.id]), {'title': 'Updated Review', 'content': 'This is an updated review.', 'rating': '1'})
        self.assertEqual(response.status_code, 302)  # Redirection to 'review_list'
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Review')

    def test_delete_review(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)  # Redirection to 'review_list'
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
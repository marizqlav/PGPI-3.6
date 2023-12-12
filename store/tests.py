from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Order, Customer
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='testcustomer@example.com')
        self.product = Product.objects.create(name='Test Product', price=10.00, stock_no=10)
        self.order = Order.objects.create(customer=self.customer, complete=False)
        self.store_url = reverse('store')
        self.cart_url = reverse('cart')
        self.checkout_url = reverse('checkout')
        self.product_detail_url = reverse('product_detail', args=[self.product.id])

    def test_store_GET(self):
        response = self.client.get(self.store_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store_main.html')

    def test_cart_GET(self):
        response = self.client.get(self.cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_checkout_GET(self):
        response = self.client.get(self.checkout_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')

    def test_product_detail_GET(self):
        response = self.client.get(self.product_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_detail.html')

    def test_edit_product_POST(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_product', args=[self.product.id]), {
            'name': 'Updated name',
            'type': 'Cuadro',
            'maker': 'Berria',
            'price': '10.00',
            'digital': False,
            'image': '',  # Aquí deberías proporcionar una imagen válida
            'stock_no': '5',
        })

        self.assertEquals(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEquals(self.product.name, 'Updated name')
        self.assertEquals(self.product.type, 'Cuadro')
        self.assertEquals(self.product.maker, 'Berria')
        self.assertEquals(self.product.price, 10.00)
        self.assertEquals(self.product.digital, False)
        self.assertEquals(self.product.stock_no, 5)
        # Asegúrate de que todos los demás campos del producto se hayan actualizado correctamente
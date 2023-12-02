from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = [
        ('PL', 'Placed'),
        ('PR', 'Processing'),
        ('SH', 'Shipped'),
        ('DE', 'Delivered'),
    ]
PRODUCT_TYPES = [
    ('Cuadro', 'Cuadro'),
    ('Manillar', 'Manillar'),
    ('Sillin', 'Sillin'),
    ('Camara', 'Camara'),
    ('Rueda', 'Rueda'),
    ('Freno', 'Freno'),
    ('Pedal', 'Pedal'),
    ('Cambios', 'Cambios'),
]

MAKER_TYPES = [
    ('Berria', 'Berria'),
    ('BH', 'BH'),
    ('CBK', 'CBK'),
    ('Goka', 'Goka'),
    ('Massi', 'Massi'),
    ('Megamo', 'Megamo'),
    ('MMR ', 'MMR '),
    ('Monty', 'Monty'),
    ('MSC', 'MSC'),
    ('Orbea', 'Orbea'),
    ('Vitoria', 'Vitoria'),
    ('Unno', 'Unno'),
]

class Customer(models.Model):
	id = models.BigAutoField(primary_key=True)  # Campo de clave primaria explícito
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def get_registered_orders(self):
		return Order.objects.filter(customer=self, customer__user__isnull=False)

	def get_guest_orders(self):
		return Order.objects.filter(customer=self, customer__user__isnull=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	id = models.BigAutoField(primary_key=True)  # Campo de clave primaria explícito
	name = models.CharField(max_length=200)
	type = models.CharField(max_length=200,choices=PRODUCT_TYPES,null=True) 
	maker = models.CharField(max_length=200,choices=MAKER_TYPES,null=True)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	stock_no = models.CharField(max_length=100, null=True, blank=True)


	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	id = models.BigAutoField(primary_key=True)  # Campo de clave primaria explícito
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')
	tracking_number = models.CharField(max_length=200, null=True, blank=True)
	estimated_delivery_date = models.DateTimeField(null=True, blank=True)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self): 
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model): 
	id = models.BigAutoField(primary_key=True)  # Campo de clave primaria explícito
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	id = models.BigAutoField(primary_key=True)  # Campo de clave primaria explícito
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
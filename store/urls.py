from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.storeMain, name="store"),
    path('catalog/', views.store, name="catalog"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('catalog/update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),
    path('guest/orders/', views.guest_orders, name='guest_orders'),
    path('customer_orders/<int:customer_id>/', views.customer_orders, name='customer_orders'),
    
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('contact/', views.contact, name='contact'),
    path('contact/enviar_correo/', views.enviar_correo, name='enviar_correo'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),


    path('create-checkout-session/', views.create_checkout_session),
    path('payment-success/', views.payment_success),
    path('payment-cancelled/', views.payment_cancelled),

    path('update_order/<int:order_id>/', views.update_order, name='update_order'),



]
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
	path('customers_orders/<int:customer_id>/', views.customer_orders, name='customers_orders'),

]
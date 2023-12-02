from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.storeMain, name="store"),
	path('catalog/', views.store, name="catalog"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]
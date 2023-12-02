from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.utils.crypto import get_random_string
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # Genera un número de seguimiento aleatorio que no esté en uso
    while True:
        tracking_number = get_random_string(length=32)
        if not Order.objects.filter(tracking_number=tracking_number).exists():
            break

    # Asigna el número de seguimiento al pedido
    order.tracking_number = tracking_number

    order.estimated_delivery_date = timezone.now() + relativedelta(months=2)


    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied
    context = {'order': order}
    return render(request, 'track_order.html', context)

@login_required
def customer_orders(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied
    registered_orders = customer.get_registered_orders()

    context = {
        'registered_orders': registered_orders,
    }

    return render(request, 'customers_orders.html', context)

@staff_member_required
def guest_orders(request):
    order_by = request.GET.get('order_by', 'id')  
    status = request.GET.get('status', '') 

    # Obtén todos los pedidos
    guest_orders = Order.objects.all()

    if status:
        guest_orders = guest_orders.filter(status=status)

    if order_by == 'get_cart_total':
        guest_orders = sorted(guest_orders, key=lambda order: order.get_cart_total)
    else:
        guest_orders = guest_orders.order_by(order_by)

    paginator = Paginator(guest_orders, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'store/guest_orders.html', context)
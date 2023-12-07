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
from django.core.mail import send_mail
from django.http import JsonResponse

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product_type = request.GET.get('product_type', 'all') or 'all'
    maker = request.GET.get('maker', 'all') or 'all'
    search = request.GET.get('search', '')

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if product_type != "all":
        products = products.filter(type=product_type)

    if maker != "all":
        products = products.filter(maker=maker)

    context = {'products':products, 'product_types': PRODUCT_TYPES, 'maker_types': MAKER_TYPES, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def storeMain(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product_type = request.GET.get('product_type', 'all') or 'all'
    maker = request.GET.get('maker', 'all') or 'all'
    search = request.GET.get('search', '')

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if product_type != "all":
        products = products.filter(type=product_type)

    if maker != "all":
        products = products.filter(maker=maker)

    context = {'products':products, 'product_types': PRODUCT_TYPES, 'maker_types': MAKER_TYPES, 'cartItems':cartItems}
    return render(request, 'store/store_main.html', context)

def storeMain(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    product_type = request.GET.get('product_type', 'all') or 'all'
    maker = request.GET.get('maker', 'all') or 'all'
    search = request.GET.get('search', '')

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if product_type != "all":
        products = products.filter(type=product_type)

    if maker != "all":
        products = products.filter(maker=maker)

    context = {'products':products, 'product_types': PRODUCT_TYPES, 'maker_types': MAKER_TYPES, 'cartItems':cartItems}
    return render(request, 'store/store_main.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	# Conjunto de tipos de productos
	product_types = set(data['types'])

    # Verifica si hay al menos un artículo de cada tipo en el carrito
	has_all_types = product_types == set([product_type[0] for product_type in PRODUCT_TYPES])
	missing_types = set([product_type[0] for product_type in PRODUCT_TYPES]) - product_types

	#context = {'items':items, 'order':order, 'cartItems':cartItems}
	context = {'items':items, 'product_types': product_types, 'order':order, 'cartItems':cartItems, 'has_all_types': has_all_types, 'missing_types': missing_types}
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
        product.stock_no = (product.stock_no - 1)
        
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.stock_no = (product.stock_no + 1)
    
    elif action == 'clear':
        product.stock_no = (product.stock_no + orderItem.quantity)
        orderItem.quantity = 0
        

    orderItem.save()
    product.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('El artículo fue añadido', safe=False)

import stripe
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/store/'
        stripe.api_key = 'sk_test_51OKWXoL9mkc6WFFaDpedWlNfgDBTtJUTd8mgHNKgUjsXQtxe5pH3M6aPlSynfnvNYXI10zqFfpUFRx1pPgOKkTRe00vVq27WZq'
        try:
            data = json.loads(request.body)
            
            price = stripe.Price.create(
                currency="eur",
                unit_amount=int(float(data['form']['total'].replace(',', '.')) * 100),
                product_data={"name": "Test"},
            )

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment-success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payment-cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    # Provide the exact Price ID (e.g. pr_1234) of the product you want to sell
                    'price': price['id'],
                    'quantity': 1
                }]
            )
            global last_session_request
            last_session_request = request
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

last_session_id = None
last_session_request = None

def payment_sucess(request):
    global last_session_id
    global last_session_request
    if request.GET['session_id'] == last_session_id:
        return
    last_session_id = request.GET['session_id']
    processOrder(last_session_request)

    return render(request, 'store/payment-sucess.html')

def payment_cancelled(request):
    return render(request, 'store/payment-cancelled.html')


def processOrder(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).order_by('-id').first()
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'].replace(',', '.'))

    if order is None and total > 0:
        order = Order.objects.create(customer=customer, complete=False)

    while True:
        transaction_id = get_random_string(length=32)
        if not Order.objects.filter(transaction_id=transaction_id).exists():
            break

    order.transaction_id = transaction_id

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

    # Actualizar el stock si el usuario no está autenticado
    if not request.user.is_authenticated:
        for item in order.orderitem_set.all():
            product = item.product
            product.stock_no -= item.quantity
            product.save()

    return JsonResponse('Pago realizado..', safe=False)

@login_required
def track_order(request, order_id):
    data = cartData(request)
    cartItems = data['cartItems']
    order = get_object_or_404(Order, id=order_id)
    if order.customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied
    context = {'order': order,'cartItems':cartItems}
    return render(request, 'store/track_order.html', context)

@login_required
def customer_orders(request, customer_id):
    data = cartData(request)
    cartItems = data['cartItems']
    customer = get_object_or_404(Customer, id=customer_id)
    if customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied

    order_by = request.GET.get('order_by', 'id')
    status = request.GET.get('status', '')
    registered_orders = customer.get_registered_orders()

    if status:
        registered_orders = registered_orders.filter(status=status)

    if order_by == 'get_cart_total':
        registered_orders = sorted(registered_orders, key=lambda order: order.get_cart_total)
    else:
        registered_orders = registered_orders.order_by(order_by)

    paginator = Paginator(registered_orders, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cartItems':cartItems,
    }

    return render(request, 'store/customers_orders.html', context)

@staff_member_required
def guest_orders(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order_by = request.GET.get('order_by', 'id')  
    status = request.GET.get('status', '') 

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
        'cartItems':cartItems,
    }

    return render(request, 'store/guest_orders.html', context)

def terms_of_use(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'store/terms_of_use.html',{'cartItems':cartItems})

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'store/contact.html',{'cartItems':cartItems})

def enviar_correo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
                
        try:
            send_mail(
                asunto,
                f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}',
                'pgpitienda@gmail.com', 
                ['pgpitienda@gmail.com'],  
                fail_silently=False,
            )
            return JsonResponse({'mensaje': 'Correo enviado correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({}, status=405)
    
def product_detail(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product,'cartItems':cartItems})

from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from .forms import ProductForm

def edit_product(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = get_object_or_404(Product, pk=product_id)
    if not request.user.is_staff:
        return render(request, 'store/permission_denied.html', {'cartItems':cartItems})
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Redireccionar a la página del producto o a donde desees
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/edit_product.html', {'product': product, 'form': form,'cartItems':cartItems})

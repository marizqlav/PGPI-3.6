from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm
import stripe
from django.views.decorators.csrf import csrf_exempt

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

	is_free = False
	if not request.user.is_authenticated:
		is_free = order['get_cart_total'] > 400.0
	
	#context = {'items':items, 'order':order, 'cartItems':cartItems}
	context = {'items':items, 'product_types': product_types, 'order':order, 'cartItems':cartItems, 'has_all_types': has_all_types, 'missing_types': missing_types, 'is_free': is_free}
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

def payment_success(request):
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
    
    try:
        # Buscar el pedido asociado a la sesión
        

        # Obtener los artículos del pedido
        order_items = OrderItem.objects.filter(order=order)
        if request.user.is_authenticated:
            # Crear el contenido del correo electrónico
            email_subject = f'Nuevo pedido - ID: {order.id}'
            email_body = f'El cliente {customer.user.first_name} {customer.user.last_name} ha realizado un nuevo pedido:\n\n'
            
            for item in order_items:
                email_body += f'Producto: {item.product.name}\n'
                email_body += f'Precio unitario: {item.product.price}€\n'
                email_body += f'Cantidad: {item.quantity}\n'
                email_body += f'Subtotal: {item.get_total}€\n\n'

            email_body += f'Total del pedido: {order.get_cart_total}€\n'
            email_body += f'Fecha del pedido: {order.date_ordered}\n'
            
            send_mail(
                email_subject,
                email_body,
                'pgpitienda@gmail.com', 
                ['pgpitienda@gmail.com', customer.user.email],  
                fail_silently=False,
            )
        else:
            name = data['form']['name']
            email = data['form']['email']
            email_subject = f'Nuevo pedido - ID: {order.id}'
            email_body = f'El cliente {name} ha realizado un nuevo pedido:\n\n'
            
            for item in order_items:
                email_body += f'Producto: {item.product.name}\n'
                email_body += f'Precio unitario: {item.product.price}€\n'
                email_body += f'Cantidad: {item.quantity}\n'
                email_body += f'Subtotal: {item.get_total}€\n\n'

            email_body += f'Total del pedido: {order.get_cart_total}€\n'
            email_body += f'Fecha del pedido: {order.date_ordered}\n'
            
            send_mail(
                email_subject,
                email_body,
                'pgpitienda@gmail.com', 
                ['pgpitienda@gmail.com', email],  
                fail_silently=False,
            )

    except Order.DoesNotExist:
        print('No se encontró el pedido asociado a la sesión.')
    except Exception as e:
        print(f'Error al enviar el correo electrónico: {str(e)}')

    return JsonResponse('Pago realizado..', safe=False)

@login_required
def track_order(request, order_id):
    data = cartData(request)
    cartItems = data['cartItems']
    order = get_object_or_404(Order, id=order_id)
    shippingAddress = ShippingAddress.objects.filter(order=order).first()
    if order.customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied
    context = {'order': order,'cartItems':cartItems, "shippingAddress":shippingAddress}
    return render(request, 'store/track_order.html', context)

def update_shipping_address(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        if order.customer != request.user.customer and not request.user.is_staff: 
            raise PermissionDenied

        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postalCode')

        
        shipping_address, created = ShippingAddress.objects.get_or_create(order=order, defaults={
            'address': street,
            'city': city,
            'state': country,
            'zipcode': postal_code,
        })

        
        if not created:
            shipping_address.address = street
            shipping_address.city = city
            shipping_address.state = country
            shipping_address.zipcode = postal_code
            shipping_address.save()

        
        return redirect('track_order', order_id=order_id)

@login_required
def customer_orders(request, customer_id):
    data = cartData(request)
    cartItems = data['cartItems']
    customer = get_object_or_404(Customer, id=customer_id)
    if customer != request.user.customer and not request.user.is_staff:
        raise PermissionDenied

    order_by = request.GET.get('order_by', 'id') or 'id'
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
    status = request.GET.get('status', '') 
    order_by = request.GET.get('order_by', 'id') or 'id'

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
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/edit_product.html', {'product': product, 'form': form,'cartItems':cartItems})


def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('guest_orders')
    return redirect('guest_orders')

def delete_product(request, product_id):
    if not request.user.is_staff:
        return render(request, 'store/permission_denied.html')  # Asegúrate de tener una plantilla para la denegación de permiso

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'El producto se eliminó exitosamente.')
        return redirect('catalog')  # Redirecciona a la página principal de la tienda o a donde sea adecuado

    return render(request, 'store/delete_product.html', {'product': product})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('catalog')  # Redirige a donde desees luego de agregar el producto
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})


from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Claim
from store.utils import cookieCart, cartData, guestOrder
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone



@login_required
def claim_list(request):
    claims = Claim.objects.filter(user=request.user)
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'claims/claim_list.html', {'claims': claims,'cartItems':cartItems})

@user_passes_test(lambda user: user.is_staff)
def claim_list_admin(request):
    data = cartData(request)
    cartItems = data['cartItems']
    claims = Claim.objects.all()
    return render(request, 'claims/claim_list_admin.html', {'claims': claims,'cartItems':cartItems})

@login_required
def claim_detail(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    data = cartData(request)
    cartItems = data['cartItems']
    if claim.user != request.user and not request.user.is_staff:
        return render(request, 'claims/claim_detail_error.html',{'cartItems':cartItems})
    return render(request, 'claims/claim_detail.html', {'claim': claim,'cartItems':cartItems})

@login_required
def claim_create(request):
    data = cartData(request)
    cartItems = data['cartItems']

    today_min = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_max = today_min + timezone.timedelta(days=1)
    user_claims_today = Claim.objects.filter(user=request.user, created_at__range=(today_min, today_max))

    if user_claims_today.count() >= 3:
        return render(request, 'claims/claim_limit_error.html',{'cartItems':cartItems})

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        claim = Claim.objects.create(user=request.user, title=title, description=description)
        return HttpResponseRedirect(reverse('claim_detail', args=(claim.id,)))
    return render(request, 'claims/claim_create.html',{'cartItems':cartItems})

@login_required
def claim_update(request, claim_id):
    data = cartData(request)
    cartItems = data['cartItems']
    claim = get_object_or_404(Claim, id=claim_id)
    if claim.user != request.user and not request.user.is_staff:
        return render(request, 'claims/claim_detail_error.html',{'cartItems':cartItems})
    if request.method == 'POST':
        claim.title = request.POST['title']
        claim.description = request.POST['description']
        if request.user.is_staff:
            claim.status = request.POST['status']
            claim.admin_feedback = request.POST['admin_feedback']
        claim.save()
        return HttpResponseRedirect(reverse('claim_detail', args=(claim.id,)))
    return render(request, 'claims/claim_update.html', {'claim': claim,'cartItems':cartItems})

@login_required
def claim_delete(request, claim_id):
    data = cartData(request)
    cartItems = data['cartItems']
    claim = get_object_or_404(Claim, id=claim_id)
    if claim.user != request.user and not request.user.is_staff:
        return render(request, 'claims/claim_detail_error.html',{'cartItems':cartItems})
    if request.method == 'POST':
        claim.delete()
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('claim_list_admin'))
        else:
            return HttpResponseRedirect(reverse('claim_list'))
    return render(request, 'claims/claim_delete.html', {'claim': claim,'cartItems':cartItems})
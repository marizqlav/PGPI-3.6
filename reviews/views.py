from django.shortcuts import render, redirect
from .models import Review
from django.contrib import messages
from store.utils import cookieCart, cartData, guestOrder
from django.shortcuts import get_object_or_404

from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    data = cartData(request)
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(user=request.user).exists()
    else:
        user_has_reviewed = False
    cartItems = data['cartItems']
    return render(request, 'review_list.html', {'reviews': reviews, 'cartItems': cartItems,'user_has_reviewed': user_has_reviewed})

def add_review(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if Review.objects.filter(user=request.user).exists():
                messages.error(request, 'Ya tenías una opinión.')
                return redirect('review_list_error')
            else:
                review = form.save(commit=False)
                review.user = request.user  # Assign the current logged-in user
                review.save()
                return redirect('review_list')
    else:
        form = ReviewForm()
        
    return render(request, 'add_review.html', {'form': form,'cartItems':cartItems})

def review_list_error(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'review_list_error.html',{'cartItems':cartItems})

def edit_review(request, review_id):
    data = cartData(request)
    cartItems = data['cartItems']
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        messages.error(request, 'No tienes permiso para editar esta opinión.')
        return redirect('review_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form,'cartItems':cartItems})

def delete_review(request, review_id):
    data = cartData(request)
    cartItems = data['cartItems']
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        messages.error(request, 'No tiene permiso para eliminar esta opinión.')
        return redirect('review_list')

    if request.method == 'POST':
        review.delete()
        return redirect('review_list')

    return render(request, 'confirm_delete.html', {'object': review,'cartItems':cartItems})
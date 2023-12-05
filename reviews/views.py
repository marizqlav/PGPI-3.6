from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_list.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the current logged-in user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})
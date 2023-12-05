from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('add_review/', views.add_review, name='add_review'),
]
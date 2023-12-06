from django.urls import path
from .views import review_list_error,add_review, review_list, edit_review, delete_review


urlpatterns = [
    path('reviews/', review_list, name='review_list'),
    path('add_review/', add_review, name='add_review'),
    path('reviews/reviews/add_review/', add_review, name='add_review'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('review_list_error/', review_list_error, name='review_list_error'),
]
from django.urls import path
from . import views

urlpatterns = [
    # ... otras rutas ...
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/admin/', views.claim_list_admin, name='claim_list_admin'),    
    path('claims/<int:claim_id>/', views.claim_detail, name='claim_detail'),
    path('claims/create/', views.claim_create, name='claim_create'),
    path('claims/<int:claim_id>/update/', views.claim_update, name='claim_update'),
    path('claims/<int:claim_id>/delete/', views.claim_delete, name='claim_delete'),
    # ... otras rutas ...
]
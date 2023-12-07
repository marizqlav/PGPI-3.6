from django.contrib import admin

from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import home, profile, RegisterView
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView, ResetPasswordView, ChangePasswordView, admin_users, user_delete,logout_view

from users.forms import LoginForm

urlpatterns = [

    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),

    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),

    path('logout/', logout_view, name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    path('admin/', admin_users),
    path('admin/delete/<str:username>', user_delete),
     path('login_error/', views.login_error, name='login_error'),

    path('admin/users/', views.admin_users, name='admin-users-list'),
    path('admin/users/create/', views.admin_create_user, name='admin-users-create'),
    path('admin/users/update/<str:username>/', views.update_user, name='admin-users-update'),
    path('admin/users/delete/<str:username>/', views.delete_user, name='admin-users-delete'),
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

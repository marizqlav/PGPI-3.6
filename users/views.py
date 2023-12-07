from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from store.utils import cookieCart, cartData, guestOrder
from store.models import Customer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from users.models import Profile

def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems':cartItems}
    return render(request, 'users/home.html',context)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        
        form = self.form_class(initial=self.initial)
        context = {'form': form,'cartItems':cartItems}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = cartData(request)
        cartItems = data['cartItems']
        if form.is_valid():
            user = form.save()

            # Crear un objeto Customer relacionado con el usuario registrado
            customer = Customer.objects.create(
                user=user,
                name=user.username,  # Puedes cambiar esto según el nombre que quieras asignar al Customer
                email=user.email  # Usa el email del usuario para el Customer
            )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')

            return redirect(to='login')
        context = {'form': form,'cartItems':cartItems}
        return render(request, self.template_name, context)


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "Hemos enviado a tu correo las instrucciones para recuperar tu contraseña, " \
                      "siempre y cuando el correo exista en nuestra base de datos. Deberías recibirlo en breve." \
                      " Si no has recibido el correo, " \
                      "por favor, asegurate de que era el mismo que usaste para tu registro y comprueba tu carpeta de spam."
    success_url = reverse_lazy('users-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Se ha actualizado tu contraseña correctamente"
    success_url = reverse_lazy('users-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        context['cartItems'] = data['cartItems']
        return context

@login_required
def profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form,'cartItems':cartItems})

@login_required
@staff_member_required
def admin_users(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'users/admin.html', {'users': Profile.objects.all(),'cartItems':cartItems})

@login_required
def user_delete(request, username):
    if request.user.is_superuser:

        profile = [i for i in Profile.objects.all() if i.user.username == username][0]

        profile.delete()
        return HttpResponse("Usuario borrado")
    else:
        return HttpResponse("Permiso denegado")
    
def login_error(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'users/login_error.html',{'cartItems':cartItems})

def logout_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    logout(request)
    return render(request,'users/logout.html',{'cartItems':cartItems}) 

from django.shortcuts import get_object_or_404

@login_required
@staff_member_required
def update_user(request, username):
    if request.user.is_staff:
        user = get_object_or_404(User, username=username)
        user_profile = Profile.objects.get(user=user)

        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Usuario actualizado correctamente')
                return redirect('admin-users-list')
        else:
            user_form = UpdateUserForm(instance=user)

        return render(request, 'users/update_user.html', {'user_form': user_form})
    else:
        return HttpResponse("Permiso denegado")
    
@login_required
@staff_member_required
def delete_user(request, username):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user__username=username)
        user = User.objects.get(username=username)
        
        # Verificar si se confirma la eliminación
        if 'confirm-delete' in request.POST:
            user_profile.delete()
            user.delete()
            messages.success(request, 'Usuario eliminado correctamente')
            return redirect('admin-users-list')
        else:
            return redirect('admin-users-list')  # Redirigir si no se confirma la eliminación
    
    return render(request, 'users/delete_user.html', {'username': username})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from users.forms import ProfileForm  # Asegúrate de tener importado correctamente el formulario de perfil
from .forms import CustomUserCreationForm


@login_required
@staff_member_required
def admin_create_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)  # Usa tu formulario personalizado
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.first_name = user_form.cleaned_data['first_name']  # Agrega el primer nombre
            user.last_name = user_form.cleaned_data['last_name']  # Agrega el apellido
            user.save()

            # Crear el Customer asociado al usuario
            customer = Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )

            return redirect('admin-users-list')  # Redirige a la lista de usuarios después de crear uno nuevo
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'users/create_user.html', {'user_form': user_form})
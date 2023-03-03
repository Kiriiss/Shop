from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from products.models import Cart, Product
from users.forms import LoginForm, RegisterForm, UserProfileForm

from users.models import User


def logout_view(request):
    logout(request)
    return redirect('products:home')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Пользователь {username} был успешно зарегистрирован!')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('products:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    return render(request, 'users/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('products:home')
        else:
            messages.error(request, 'Имя пользователя или пароль неверны.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def elit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'title': 'Shop - профиль ',

    }
    return render(request, 'users/edit_profile.html', context)


def profile(request):
    context = {

        'title': 'Shop - профиль ',
        'baskets': Cart.objects.filter(user=request.user),
        'all_products': Product.objects.all()
    }
    return render(request, 'users/user_profile.html', context)


def delete_from_cart(request, basket_id):
    basket = Cart.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

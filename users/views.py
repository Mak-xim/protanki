from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

from protanki_web.settings import DEFAULT_FROM_EMAIL
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash




def send_activation_email(request, user):
    """Отправляет письмо со ссылкой для активации аккаунта."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Подтверждение регистрации'
    message = (
        f'Здравствуйте, {user.username}!\n\n'
        f'Подтвердите регистрацию, перейдя по ссылке:\n{activation_link}\n\n'
        f'Если вы не регистрировались, проигнорируйте это письмо.'
    )
    send_mail(subject, message, 'noreply@protanki.com', [user.email])


def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Блокируем вход до подтверждения по email
            user.save()
            send_activation_email(request,user)
            messages.success(request, 'Письмо с подтверждением отправлено на вашу почту.')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    """Активация аккаунта по ссылке из письма."""
    user_model = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Автоматически логиним пользователя
        messages.success(request, 'Ваш аккаунт активирован! Вы вошли в систему.')
    else:
        messages.error(request, 'Ссылка активации недействительна или устарела.')

    return redirect('index')

def logout_view(request):
    """Выход из аккаунта."""
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_model = get_user_model()  # Используем lowercase с подчёркиванием

        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user = None

        if user is not None and not user.is_active:
            send_activation_email(request, user)
            messages.warning(request, 'Сначала подтвердите свою почту. Мы отправили вам новое письмо.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль.')

        form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request:HttpRequest):
    if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('profile')
            else:
                messages.error(request, 'Ничего не удается ')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {
        'form': form,
    })

@login_required
def send_password_reset(request):
    user = request.user
    if not user.email:
        messages.error(request, "У вашего аккаунта не указана почта.")
        return redirect('profile')  # или куда угодно

    form = PasswordResetForm({'email': user.email})
    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=DEFAULT_FROM_EMAIL,  # можно задать DEFAULT_FROM_EMAIL в settings.py
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt',
        )
        messages.success(request, "Письмо для смены пароля отправлено на вашу почту.")
        return redirect('password_reset_done')
    else:
        messages.error(request, "Не удалось отправить письмо. Проверьте настройки.")
        return redirect('profile')

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # чтобы не разлогинивало
            messages.success(request, "Пароль успешно изменён!")
            return redirect("profile")  # имя твоей страницы профиля
        else:
            messages.error(request, "Исправьте ошибки ниже.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})


from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from django.contrib.auth.models import User  # для аннотации типа User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from protanki_web.settings import DEFAULT_FROM_EMAIL

from .forms import ProfileForm, UserRegisterForm


def send_activation_email(request: HttpRequest, user: User) -> None:
    """Отправляет письмо со ссылкой для активации аккаунта."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse("activate_account", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Подтверждение регистрации"
    message = (
        f"Здравствуйте, {user.username}!\n\n"
        f"Подтвердите регистрацию, перейдя по ссылке:\n{activation_link}\n\n"
        f"Если вы не регистрировались, проигнорируйте это письмо."
    )
    send_mail(subject, message, "noreply@protanki.com", [user.email])


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Блокируем вход до подтверждения по email
            user.save()
            send_activation_email(request, user)
            messages.success(
                request, "Письмо с подтверждением отправлено на вашу почту."
            )
            return redirect("index")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def activate_account(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
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
        messages.success(request, "Ваш аккаунт активирован! Вы вошли в систему.")
    else:
        messages.error(request, "Ссылка активации недействительна или устарела.")

    return redirect("index")


def logout_view(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта."""
    logout(request)
    return redirect("index")


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user = None

        if user is not None and not user.is_active:
            send_activation_email(request, user)
            messages.warning(
                request,
                "Сначала подтвердите свою почту. Мы отправили вам новое письмо.",
            )
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Неверный логин или пароль.")

        form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("profile")
        else:
            messages.error(request, "Ничего не удается ")
    else:
        form = ProfileForm(instance=request.user)
    return render(
        request,
        "users/profile.html",
        {
            "form": form,
        },
    )


@login_required
def send_password_reset(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not user.email:
        messages.error(request, "У вашего аккаунта не указана почта.")
        return redirect("profile")

    form = PasswordResetForm({"email": user.email})
    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=DEFAULT_FROM_EMAIL,
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        )
        messages.success(request, "Письмо для смены пароля отправлено на вашу почту.")
        return redirect("password_reset_done")
    else:
        messages.error(request, "Не удалось отправить письмо. Проверьте настройки.")
        return redirect("profile")


@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # чтобы не разлогинивало
            messages.success(request, "Пароль успешно изменён!")
            return redirect("profile")
        else:
            messages.error(request, "Исправьте ошибки ниже.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})

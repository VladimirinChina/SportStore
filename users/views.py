from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm


def register(request):
    """Регистрирует нового пользователя."""

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            send_mail(
                subject="Добро пожаловать в SportStore!",
                message=(
                    f"Здравствуйте!\n\n"
                    f"Вы успешно зарегистрировались в SportStore "
                    f"с адресом {user.email}.\n\n"
                    f"Добро пожаловать!"
                ),
                from_email=None,
                recipient_list=[user.email],
            )

            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def user_login(request):
    """Выполняет вход пользователя."""

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})

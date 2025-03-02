from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

def index(request):
    return HttpResponse("Hello, world! You're at the polls index.")

def calculate_cost(request):
    result = ""

    if request.method == 'POST':
        price = float(request.POST.get('price', 0))
        weight = float(request.POST.get('weight', 0))
        result = round(price * weight, 2)

    return render(request, 'testapp/calculate_cost.html', {'result': result})
def index(request):
    return render(request, 'testapp/index.html')

def aud1(request):
    result = ""
    weight = ""
    Clear = True
    if request.method == 'POST':
        if 'calculate' in request.POST:
            try:
                weight = float(request.POST.get('weight'))
                result = round(6 * pow(weight, 2), 2)
                if weight <= 0:
                    weight = ""
                    raise ValueError("Ошибка ввода!")
            except ValueError as e:
                result = f"{e}"
        elif 'clear' in request.POST:
            Clear = False
    return render(request, 'testapp/aud1.html', {
        'weight': weight,
        'result': result,
    })

def calculate_parallelepiped(request):
    result = ""
    length = ""
    width = ""
    height = ""
    clear = True

    if request.method == 'POST':
        if 'calculate' in request.POST:
            try:
                length = float(request.POST.get('length'))
                width = float(request.POST.get('width'))
                height = float(request.POST.get('height'))

                if length <= 0 or width <= 0 or height <= 0:
                    raise ValueError("Ошибка ввода! Все значения должны быть положительными.")

                result = round(length * width * height, 2)
            except ValueError as e:
                result = str(e)
        elif 'clear' in request.POST:
            clear = False

    return render(request, 'testapp/calculate_parallelepiped.html', {
        'length': length,
        'width': width,
        'height': height,
        'result': result,
    })
def landing(request):
    return render(request, 'view/landing.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("landing")

    return render(request, "auth/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect('landing')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/profile.html', {'form': form})

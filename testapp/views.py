from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, OrderForm, ProfileForm, LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Order

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
            user = form.save()

            # ✅ Создаём профиль сразу после регистрации
            Profile.objects.create(user=user)

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
            return redirect(resolve_url("landing"))  # <-- Убедись, что "landing" есть в urls.py

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

def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Перенаправляем на список заказов
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})

CATEGORY_CHOICES = [
    ('phones', 'Телефоны и гаджеты'),
    ('appliances', 'Бытовая техника'),
    ('tv_audio', 'ТВ, Аудио и Видео'),
    ('computers', 'Компьютеры'),
    ('home_goods', 'Товары для дома'),
]

def order_list(request):
    category = request.GET.get('category')  # Получаем категорию из запроса
    orders = Order.objects.all()

    if category:
        orders = orders.filter(category=category)  # Фильтруем заказы

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'categories': CATEGORY_CHOICES,
    })

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
    return redirect('order_list')

# Форма редактирования заказа (страница отдельно)
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})
from datetime import timezone
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from .models import CartItem, Customer, Delivery, Order, OrderItem, Product
from bakery_app.utils import CustomDecimalEncoder
import json
from django.contrib.auth import logout

# Главная страница
def home(request):
    return render(request, 'bakery_app/home.html')

# Страница корзины
def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Вы должны быть авторизованы для просмотра корзины.")
        return redirect('login')

    cart_items = CartItem.objects.filter(customer=request.user)
    total_amount = sum(item.total_price for item in cart_items)  # Общая сумма

    return render(request, 'bakery_app/cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

# Страница доставки
def delivery_detail(request, delivery_id):
    try:
        delivery = get_object_or_404(Delivery, id=delivery_id, customer=request.user)
    except Delivery.DoesNotExist:
        messages.error(request, "У вас нет доставок.")
        return redirect('home')  # Перенаправление на домашнюю страницу или другую

    return render(request, 'bakery_app/delivery_detail.html', {'delivery': delivery})



# Страница каталога
def catalog(request):
    products = Product.objects.all()  # Получаем все продукты из базы данных
    return render(request, 'bakery_app/catalog.html', {'products': products})

# Вход в систему
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный email или пароль.')

    return render(request, 'bakery_app/login.html')

# Регистрация нового пользователя
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Customer.objects.filter(phone=phone).exists():
            messages.error(request, 'Этот номер телефона уже зарегистрирован.')
            return render(request, 'bakery_app/register.html')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Этот email уже зарегистрирован.')
            return render(request, 'bakery_app/register.html')

        try:
            customer = Customer.objects.create_user(
                username=email, 
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
            )
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, попробуйте еще раз.')
            return render(request, 'bakery_app/register.html')

    return render(request, 'bakery_app/register.html')

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Вы должны быть авторизованы для добавления товара в корзину.")
        return redirect('login')
    
    # Получаем товар по ID
    product = get_object_or_404(Product, id=product_id)

    # Если товар уже есть в корзине
    cart_item, created = CartItem.objects.get_or_create(
        customer=request.user, product=product
    )

    if not created:
        cart_item.quantity += 1  # Увеличиваем количество товара
        cart_item.save()

    messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
    return redirect('cart')

# Оформление заказа
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = CartItem.objects.filter(customer=request.user)
    
    if not cart_items:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cart')

    total_amount = sum(item.total_price for item in cart_items)

    # Создаем заказ
    order = Order.objects.create(
        customer=request.user,
        total_amount=total_amount
    )

    # Перемещаем товары из корзины в заказ
    for item in cart_items:
        order.items.create(
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Очистка корзины
    cart_items.delete()

    # Получаем данные из формы
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_address = request.POST.get('delivery_address')

        # Создание объекта доставки
        delivery = Delivery.objects.create(
            order=order,
            customer=request.user,
            delivery_date=timezone.now(),  # Можно установить дату доставки
            status='Ожидает',
            payment_method=payment_method,
            delivery_address=delivery_address
        )

        messages.success(request, f'Заказ на сумму {total_amount}₽ успешно оформлен!')

        # Перенаправление на страницу с деталями доставки
        return redirect('delivery_detail', delivery_id=delivery.id)  # Убедитесь, что это правильный редирект

    return render(request, 'bakery_app/order_detail.html', {'order': order})


def profile_view(request):
    # Если пользователь не авторизован, перенаправляем на страницу входа
    if not request.user.is_authenticated:
        return redirect('login')

    # Получаем информацию о пользователе
    customer = request.user

    return render(request, 'bakery_app/profile.html', {'customer': customer})

# Выход из системы
def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')  # Перенаправляем на страницу входа

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, customer=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

# Уменьшение количества товара в корзине
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, customer=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

# Удаление товара из корзины
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, customer=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины.')
    return redirect('cart')

def order_detail(request, order_id):
    # Получаем заказ по ID
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'bakery_app/order_detail.html', {'order': order})

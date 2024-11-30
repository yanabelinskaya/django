from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from bakery_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('delivery/<int:delivery_id>/', views.delivery_detail, name='delivery_detail'),
    path('profile/', views.profile_view, name='profile'),  # Маршрут для страницы профиля
    path('logout/', views.logout_view, name='logout'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]


# Настройки для работы с медиа-файлами (например, изображениями товаров)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

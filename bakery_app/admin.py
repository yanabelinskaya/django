from django.contrib import admin
from .models import Bakery, Product, Customer, Order, Delivery

admin.site.register(Bakery)
admin.site.register(Order)
admin.site.register(Delivery)

# Регистрируем модель Customer в админке
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'is_active')  # Отображаем эти поля в списке
    search_fields = ('full_name', 'email', 'phone')  # Добавляем возможность поиска по этим полям
    list_filter = ('is_active',)  # Добавляем фильтрацию по активности пользователя

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'image')  # Отображаем поля в списке
    search_fields = ('name', 'category')  # Возможность поиска по этим полям
    list_filter = ('category',)  # Фильтрация товаров по категориям
    list_editable = ('price',)  # Позволяет редактировать цену прямо в списке
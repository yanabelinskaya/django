# Generated by Django 5.1.3 on 2024-11-29 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0006_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_address',
            field=models.TextField(default='email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery',
            name='payment_method',
            field=models.CharField(default='Не указан', max_length=50),
            preserve_default=False,
        ),
    ]

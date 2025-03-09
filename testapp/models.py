from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


CATEGORY_CHOICES = [
    ('phones_gadgets', 'Телефоны и гаджеты'),
    ('home_appliances', 'Бытовая техника'),
    ('tv_audio_video', 'ТВ, Аудио и Видео'),
    ('computers', 'Компьютеры'),
    ('home_goods', 'Товары для дома'),
]

BRAND_CHOICES = {
    'phones_gadgets': [
        ('apple', 'Apple'),
        ('samsung', 'Samsung'),
        ('huawei', 'Huawei'),
        ('lenovo', 'Lenovo'),
        ('xiaomi', 'Xiaomi'),
    ],
    'home_appliances': [
        ('lg', 'LG'),
        ('bosch', 'Bosch'),
        ('samsung', 'Samsung'),
    ],
    'tv_audio_video': [
        ('sony', 'Sony'),
        ('samsung', 'Samsung'),
        ('lg', 'LG'),
    ],
    'computers': [
        ('asus', 'Asus'),
        ('hp', 'HP'),
        ('dell', 'Dell'),
    ],
    'home_goods': [
        ('ikea', 'IKEA'),
        ('hoff', 'Hoff'),
    ],
}

class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    brand = models.CharField(max_length=50, blank=True, null=True)  # Убрали `choices`
    image = models.ImageField(upload_to='order_images/', blank=True, null=True)

    def __str__(self):
        return self.titl

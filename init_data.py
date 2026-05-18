"""Скрипт создания начальных данных"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate.settings')
django.setup()

from django.contrib.auth.models import User
from listings.models import Category

# Создаём категории
categories = [
    ('Квартиры', 'kvartiry'),
    ('Дома / коттеджи', 'doma-kottedzhi'),
    ('Участки', 'uchastki'),
    ('Коммерческая недвижимость', 'kommercheskaya-nedvizhimost'),
]

for name, slug in categories:
    Category.objects.get_or_create(name=name, defaults={'slug': slug})
    print(f'Категория "{name}" создана.')

# Создаём суперпользователя
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан: admin / admin123')
else:
    print('Суперпользователь уже существует.')

print('Готово!')

"""Скрипт начальной настройки проекта"""
from PIL import Image, ImageDraw

# Создаём placeholder изображение
img = Image.new('RGB', (400, 300), '#eeeeee')
d = ImageDraw.Draw(img)
d.text((150, 140), 'No Photo', fill='#999999')
img.save('static/images/placeholder.png')
print('Placeholder создан.')

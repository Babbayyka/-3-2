from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """Категория недвижимости"""
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Listing(models.Model):
    """Объявление о недвижимости"""

    DEAL_TYPE_CHOICES = [
        ('sale', 'Продажа'),
        ('purchase', 'Покупка'),
    ]

    title = models.CharField(
        'Заголовок',
        max_length=200,
        validators=[MinLengthValidator(10)]
    )
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField(
        'Описание',
        max_length=5000,
        validators=[MinLengthValidator(30)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='listings'
    )
    deal_type = models.CharField(
        'Тип сделки',
        max_length=10,
        choices=DEAL_TYPE_CHOICES
    )
    price = models.DecimalField(
        'Цена (руб.)',
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(999999999.99)
        ]
    )
    area = models.DecimalField(
        'Площадь (м²)',
        max_digits=7,
        decimal_places=1,
        validators=[
            MinValueValidator(0.1),
            MaxValueValidator(99999.9)
        ]
    )
    rooms = models.PositiveIntegerField(
        'Количество комнат',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    city = models.CharField('Город', max_length=100)
    district = models.CharField('Район', max_length=100, blank=True)
    address = models.CharField('Адрес', max_length=300)
    phone = models.CharField('Телефон для связи', max_length=20)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='listings'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            if not base_slug:
                base_slug = 'listing'
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)


class Favorite(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='favorited_by'
    )
    added_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ['user', 'listing']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} — {self.listing.title}"


class ListingPhoto(models.Model):
    """Фотография объявления"""
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='photos'
    )
    photo = models.ImageField('Фотография', upload_to='listings/')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    def __str__(self):
        return f"Фото {self.order} - {self.listing.title}"

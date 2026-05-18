import django_filters
from .models import Listing, Category


class ListingFilter(django_filters.FilterSet):
    deal_type = django_filters.ChoiceFilter(
        choices=Listing.DEAL_TYPE_CHOICES,
        label='Тип сделки',
        empty_label='Все'
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все'
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Цена от'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Цена до'
    )
    area_min = django_filters.NumberFilter(
        field_name='area',
        lookup_expr='gte',
        label='Площадь от'
    )
    area_max = django_filters.NumberFilter(
        field_name='area',
        lookup_expr='lte',
        label='Площадь до'
    )
    rooms = django_filters.NumberFilter(
        field_name='rooms',
        label='Комнат'
    )
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
        label='Город'
    )
    district = django_filters.CharFilter(
        field_name='district',
        lookup_expr='icontains',
        label='Район'
    )

    class Meta:
        model = Listing
        fields = ['deal_type', 'category', 'price_min', 'price_max',
                  'area_min', 'area_max', 'rooms', 'city', 'district']

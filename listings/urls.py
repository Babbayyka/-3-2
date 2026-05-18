from django.urls import path, register_converter

from . import views
from .converters import UnicodeSlugConverter

register_converter(UnicodeSlugConverter, 'unicode_slug')

urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/<unicode_slug:slug>/', views.listing_detail_view, name='listing_detail'),
    path('listings/create/', views.listing_create_view, name='listing_create'),
    path('listings/<unicode_slug:slug>/edit/', views.listing_update_view, name='listing_update'),
    path('listings/<unicode_slug:slug>/delete/', views.listing_delete_view, name='listing_delete'),
    path('listings/<unicode_slug:slug>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('favorites/', views.favorites_view, name='favorites'),
]

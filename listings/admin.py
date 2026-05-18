from django.contrib import admin
from .models import Category, Listing, ListingPhoto, Favorite


class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 1
    max_num = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'deal_type', 'price', 'city', 'author', 'created_at', 'is_active']
    list_filter = ['category', 'deal_type', 'is_active', 'city']
    search_fields = ['title', 'description', 'city', 'address']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ListingPhotoInline]
    list_editable = ['is_active']
    date_hierarchy = 'created_at'

    def delete_queryset(self, request, queryset):
        """Удаление с каскадным удалением фотографий"""
        for listing in queryset:
            listing.photos.all().delete()
        queryset.delete()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'listing__title']
    date_hierarchy = 'added_at'

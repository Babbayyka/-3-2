from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Listing, Category, Favorite
from .forms import SearchForm, ListingForm, ListingPhotoFormSet
from .filters import ListingFilter


def home_view(request):
    """Главная страница"""
    listings = Listing.objects.filter(is_active=True).select_related('category')[:10]
    form = SearchForm()
    return render(request, 'listings/home.html', {
        'listings': listings,
        'form': form,
    })


def catalog_view(request):
    """Каталог с фильтрацией, сортировкой и пагинацией"""
    queryset = Listing.objects.filter(is_active=True).select_related('category', 'author')

    # Поиск
    search_query = request.GET.get('q', '')
    if search_query and len(search_query) >= 2:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Фильтрация
    listing_filter = ListingFilter(request.GET, queryset=queryset)
    filtered_qs = listing_filter.qs

    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        '-created_at': '-created_at',
        'created_at': 'created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'area_asc': 'area',
        'area_desc': '-area',
    }
    order_by = valid_sorts.get(sort, '-created_at')
    filtered_qs = filtered_qs.order_by(order_by)

    # Пагинация
    paginator = Paginator(filtered_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/catalog.html', {
        'filter': listing_filter,
        'page_obj': page_obj,
        'search_query': search_query,
        'current_sort': sort,
    })


def listing_detail_view(request, slug):
    """Карточка объекта"""
    listing = get_object_or_404(Listing, slug=slug, is_active=True)
    photos = listing.photos.all()
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'photos': photos,
    })


@login_required
def listing_create_view(request):
    """Создание объявления"""
    if request.method == 'POST':
        form = ListingForm(request.POST)
        formset = ListingPhotoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            formset.instance = listing
            formset.save()
            messages.success(request, 'Объявление успешно опубликовано!')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm()
        formset = ListingPhotoFormSet()
    return render(request, 'listings/listing_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Подать объявление',
    })


@login_required
def listing_update_view(request, slug):
    """Редактирование объявления"""
    listing = get_object_or_404(Listing, slug=slug)
    if listing.author != request.user:
        return HttpResponseForbidden('У вас нет прав для редактирования этого объявления.')

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        formset = ListingPhotoFormSet(request.POST, request.FILES, instance=listing)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm(instance=listing)
        formset = ListingPhotoFormSet(instance=listing)
    return render(request, 'listings/listing_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Редактировать объявление',
        'listing': listing,
    })


@login_required
def listing_delete_view(request, slug):
    """Удаление объявления"""
    listing = get_object_or_404(Listing, slug=slug)
    if listing.author != request.user:
        return HttpResponseForbidden('У вас нет прав для удаления этого объявления.')

    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Объявление удалено.')
        return redirect('dashboard')
    return render(request, 'listings/listing_confirm_delete.html', {
        'listing': listing,
    })


@login_required
def dashboard_view(request):
    """Личный кабинет"""
    listings = Listing.objects.filter(author=request.user).select_related('category')
    return render(request, 'listings/dashboard.html', {
        'listings': listings,
    })


@login_required
def toggle_favorite_view(request, slug):
    """Добавить/убрать из избранного"""
    listing = get_object_or_404(Listing, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
        messages.info(request, 'Убрано из избранного.')
    else:
        messages.success(request, 'Добавлено в избранное!')
    # Вернуться на предыдущую страницу
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@login_required
def favorites_view(request):
    """Список избранного"""
    favorites = Favorite.objects.filter(user=request.user).select_related('listing', 'listing__category')
    return render(request, 'listings/favorites.html', {
        'favorites': favorites,
    })

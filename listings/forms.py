from django import forms
from django.forms import inlineformset_factory
from .models import Listing, ListingPhoto


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по объявлениям...',
            'class': 'search-input'
        }),
        error_messages={
            'min_length': 'Минимальная длина запроса — 2 символа.',
        }
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'deal_type',
                  'price', 'area', 'rooms', 'city', 'district', 'address', 'phone']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок объявления'}),
            'description': forms.Textarea(attrs={'placeholder': 'Подробное описание объекта', 'rows': 5}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена в рублях', 'min': 1}),
            'area': forms.NumberInput(attrs={'placeholder': 'Площадь в м²', 'min': 1}),
            'rooms': forms.NumberInput(attrs={'placeholder': 'Количество комнат', 'min': 1, 'max': 99}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'district': forms.TextInput(attrs={'placeholder': 'Район (необязательно)'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон для связи'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError('Заголовок должен содержать минимум 10 символов.')
        if len(title) > 100:
            raise forms.ValidationError('Заголовок не должен превышать 100 символов.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 30:
            raise forms.ValidationError('Описание должно содержать минимум 30 символов.')
        if len(description) > 3000:
            raise forms.ValidationError('Описание не должно превышать 3000 символов.')
        return description


class ListingPhotoForm(forms.ModelForm):
    class Meta:
        model = ListingPhoto
        fields = ['photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Проверка размера (10 МБ)
            if photo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 10 МБ.')
            # Проверка формата
            allowed_types = ['image/jpeg', 'image/png']
            if photo.content_type not in allowed_types:
                raise forms.ValidationError('Допустимые форматы: JPEG, PNG.')
        return photo


ListingPhotoFormSet = inlineformset_factory(
    Listing,
    ListingPhoto,
    form=ListingPhotoForm,
    extra=3,
    max_num=10,
    can_delete=True
)

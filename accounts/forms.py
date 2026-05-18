import re
from django import forms
from django.contrib.auth.models import User


class CustomRegistrationForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        min_length=3,
        max_length=30,
        help_text='От 3 до 30 символов. Только буквы, цифры и символ подчёркивания.'
    )
    email = forms.EmailField(
        label='Email',
        max_length=254
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput,
        help_text='От 8 до 128 символов. Минимум 1 заглавная, 1 строчная буква и 1 цифра.'
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError(
                'Имя пользователя может содержать только буквы, цифры и символ подчёркивания.'
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Пароль должен содержать минимум одну заглавную букву.')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('Пароль должен содержать минимум одну строчную букву.')
        if not re.search(r'\d', password):
            raise forms.ValidationError('Пароль должен содержать минимум одну цифру.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user

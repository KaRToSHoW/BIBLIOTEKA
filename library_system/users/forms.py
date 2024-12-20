from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, ImageOption

class ClientForm(UserCreationForm):
    GENDER_CHOICES = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]

    phone_number = forms.CharField(
        max_length=15,
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона*'}),
        required=True
    )
    first_name = forms.CharField(
        max_length=128,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя*'}),
        required=True
    )
    last_name = forms.CharField(
        max_length=128,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия*'}),
        required=True
    )
    second_name = forms.CharField(
        max_length=128,
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество*'}),
        required=False,
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата рождения*'}),
        required=True,
        label='Дата рождения'
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Пол',
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Пол*'}),
        required=True
    )
    profile_image = forms.ModelChoiceField(
        queryset=ImageOption.objects.all(),
        label='Изображение профиля',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username',  'last_name', 'first_name',  'second_name', 'email', 'phone_number', 'birth_date', 'gender', 'profile_image', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль*'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля*'}),
        }

    def save(self, commit=True):
        user = super(ClientForm, self).save(commit=False)
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                second_name=self.cleaned_data['second_name'],
                birth_date=self.cleaned_data['birth_date'],
                gender=self.cleaned_data['gender'],
                profile_image=self.cleaned_data.get('profile_image')
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя*', 'name': 'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль*', 'name': 'password'}))

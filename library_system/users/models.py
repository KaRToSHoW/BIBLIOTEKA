from django.contrib.auth.models import User
from django.db import models

class ImageOption(models.Model):
    image = models.ImageField(upload_to='main/static/main/img/profile_img', verbose_name="Доступное изображение")

    class Meta:
        verbose_name = 'Доступное изображение'
        verbose_name_plural = 'Доступные изображения'

    def __str__(self):
        return f"Image {self.pk}"

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name="Телефон", blank=True)
    first_name = models.CharField(max_length=128, verbose_name="Имя", blank=True)
    last_name = models.CharField(max_length=128, verbose_name="Фамилия", blank=True)
    second_name = models.CharField(max_length=128, verbose_name="Отчество", blank=True)
    birth_date = models.DateField(null=True, verbose_name="Дата рождения", blank=True)
    gender = models.CharField(max_length=1, verbose_name="Пол", choices=GENDER_CHOICES, blank=True)
    profile_image = models.ForeignKey(ImageOption, on_delete=models.SET_NULL, null=True, verbose_name="Изображение профиля")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        first_name = self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        full_name = f'{first_name} {last_name}'.strip()
        return full_name

    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.image.url
        return None

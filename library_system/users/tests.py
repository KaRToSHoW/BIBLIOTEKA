from django.test import TestCase
from django.contrib.auth.models import User
from .models import ImageOption, Client
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class ImageOptionModelTest(TestCase):
    def setUp(self):
        self.image_option = ImageOption.objects.create(
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_image_option_creation(self):
        self.assertTrue(self.image_option.image)

    def test_image_option_str(self):
        self.assertEqual(str(self.image_option), f"Image {self.image_option.pk}")

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.image_option = ImageOption.objects.create(
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.client = Client.objects.create(
            user=self.user,
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            second_name='Middle',
            birth_date='1990-01-01',
            gender='M',
            profile_image=self.image_option
        )

    def test_client_creation(self):
        self.assertEqual(self.client.user, self.user)
        self.assertEqual(self.client.phone_number, '1234567890')
        self.assertEqual(self.client.first_name, 'John')
        self.assertEqual(self.client.last_name, 'Doe')
        self.assertEqual(self.client.second_name, 'Middle')
        birth_date = datetime.datetime.strptime(self.client.birth_date, '%Y-%m-%d').date()
        self.assertEqual(birth_date, datetime.date(1990, 1, 1))
        self.assertEqual(self.client.gender, 'M')
        self.assertEqual(self.client.profile_image, self.image_option)
        self.assertIsInstance(self.client.created_at, timezone.datetime)

    def test_client_str(self):
        self.assertEqual(str(self.client), 'John Doe')

    def test_client_str_without_names(self):
        user2 = User.objects.create_user(username='testuser2', password='12345')
        client_no_name = Client.objects.create(user=user2)
        self.assertEqual(str(client_no_name), '')

    def test_get_profile_image_url(self):
        self.assertEqual(self.client.get_profile_image_url(), self.image_option.image.url)

    def test_get_profile_image_url_no_image(self):
        user2 = User.objects.create_user(username='testuser3', password='12345')
        client_no_image = Client.objects.create(user=user2)
        self.assertIsNone(client_no_image.get_profile_image_url())

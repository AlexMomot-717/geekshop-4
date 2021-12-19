from django.test import TestCase
from django.test.client import Client

# from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self):
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            username='django',
            password='geekbrains',
        )

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)


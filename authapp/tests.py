from django.test import TestCase
from django.test.client import Client

# from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekbrains'


    def setUp(self):
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
        )

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'ПОЛЬЗОВАТЕЛЬ', status_code=self.status_ok)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get('/')
        self.assertContains(response, 'ПОЛЬЗОВАТЕЛЬ', status_code=self.status_ok)

    # def test_register(self):


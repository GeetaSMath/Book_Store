from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('registration')
        self.login_url = reverse('loginapi')
        self.book_curd = reverse('bookapi')

        self.client = APIClient()
        data = {
            "username": "geeta",
            "email": "meghana@gmail.com",
            "password": "geeta",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth"
        }
        response = self.client.post(self.register_url, data=data)
        book_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth",
            "is_superuser": True
        }
        response = self.client.post(self.book_curd, data=book_data)

    def tearDown(self):
        return super().tearDown()

from django.urls import reverse
from tests.test_setup import TestSetUp


# Create your tests here.
class UserRegistrationTestCase(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_user_registration_with_data(self):
        user_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth"
        }

        response = self.client.post(self.register_url, data=user_data)

        self.assertEqual(response.status_code, 201)

    def test_user_registration_empty_location(self):
        data = {
            "username": "",
            "email": "megh@gmail.com",
            "password": "nikita",
            "phone": "123",
            "location": "",
            "first_name": "math",
            "last_name": "math"
        }
        response = self.client.post(self.register_url, data=data)
        self.assertEqual(response.status_code, 400)


class LoginTestCase(TestSetUp):
    def test_user_login_success(self):
        user_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth"
        }

        response = self.client.post(self.register_url, data=user_data)
        # print(response.data)
        login_data = {
            'username': "meghagg",
            'password': "nikita"
        }
        response = self.client.post(self.login_url, login_data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        return response.data

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'meghagg',
            'password': 'sakshi'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 400)  # we will Expect an unauthorized response

    def test_user_login_missing_fields(self):
        # to test a login with missing fields
        login_data = {
            'username': 'priyanka'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 400)


class TestBook(TestSetUp):
    def test_book(self):
        user_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth",
            "is_superuser": True

        }

        self.client.post(self.register_url, data=user_data)
        login_data = {
            'username': "meghagg",
            'password': "nikita"
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data.get('token')
        self.client.credentials(HTTP_TOKEN=token)
        book_data = {
            "author": "martin",
            "title": "study",
            "price": 500,
            "quantity": 2
        }
        response = self.client.post(self.book_curd, book_data)
        self.assertEqual(response.status_code, 201)

    def test_book_with_invalid_data(self):
        user_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth",
        }

        self.client.post(self.register_url, data=user_data)
        login_data = {
            'username': "meghagg",
            'password': "nikita"
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data.get('token')
        headers = {
            "HTTP_TOKEN": token
        }
        book_data = {
            "author": "martin",
            "title": "study",
            "price": 500,
            "quantity": 2
        }
        response = self.client.post(self.book_curd, book_data, **headers)
        self.assertEqual(response.status_code, 400)

    def test_book_update(self):
        user_data = {
            "username": "meghagg",
            "email": "meghana@gmail.com",
            "password": "nikita",
            "phone": "7896",
            "location": "banglore",
            "first_name": "math",
            "last_name": "matth",
            "is_superuser": True

        }

        self.client.post(self.register_url, data=user_data)
        login_data = {
            'username': "meghagg",
            'password': "nikita"
        }
        response = self.client.post(self.login_url, login_data)
        token = response.data.get('token')
        self.client.credentials(HTTP_TOKEN=token)
        book_data = {
            "author": "martin",
            "title": "study",
            "price": 500,
            "quantity": 2
        }
        response = self.client.post(self.book_curd, book_data)
        id = response.data.get("data").get('id')
        book_data_up = {
            "id": 2,
            "author": "naid",
            "title": "studdied",
            "price": 200,
            "quantity": 2
        }
        self.update_book_url = reverse('bookapi')
        response = self.client.put(self.update_book_url, book_data_up)
        self.assertEqual(response.status_code, 201)

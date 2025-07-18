from django.test import TestCase

from users.models import User
from users.tests.factories import UserFactory


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "/login"
        cls.data = {"username": "username", "password": "thiscool123"}

    def test_invalid_user(self):
        """login with invalid/non existing credentials"""

        resp = self.client.post(
            self.url,
            self.data,
        )
        self.assertIn(b"Please enter a correct username and password.", resp.content)

    def test_login(self):
        """Login with correct credentials"""

        # create user
        User.objects.create_user(**self.data, email="username@gmail.com")
        resp = self.client.post(self.url, self.data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/")


class SignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.url = "/signup"
        cls.data = {
            "email": "email@example.com",
            "username": "miracle",
            "password": "password",
            "confirm_password": "password",
        }

    def test_user_creation(self):
        """Test create new user"""

        resp = self.client.post(self.url, self.data)
        # creates user and redirects to login
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/login")

    def test_validates_existing_username_and_email(self):
        """
        Assert users cannot create acct with existing emails or username
        """
        del self.data["confirm_password"]
        UserFactory(**self.data)

        self.data["confirm_password"] = self.data["password"]
        resp = self.client.post(self.url, self.data)

        self.assertIn(b"This email address is already registered", resp.content)
        self.assertIn(b"This username is already registered", resp.content)

from django.test import TestCase

from users.tests.factories import UserFactory


class UserTest(TestCase):
    def test_model_creation(self):
        """Assert that the User model was created properly"""

        user = UserFactory()

        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertIsNotNone(user.password)

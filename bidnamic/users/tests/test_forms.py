from django.test import TestCase

from users.forms import SignupForm


class SignupFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "miracle",
            "email": "miracle@gmail.com",
            "password": "password",
            "confirm_password": "password",
        }
        self.form_class = SignupForm

    def test_signup_form(self):
        """
        Assert that signup form works as expected
        """

        form = self.form_class(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """
        Assert password mismatch is validated
        """

        self.form_data["confirm_password"] = "alter password"
        form = self.form_class(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "The password and password confirmation do not match",
        )

    def test_password_lenth_validation(self):
        """
        Assert that password length is validated
        """

        self.form_data["password"] = "pass"  # less than 6 characters
        form = self.form_class(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "The password is too short, minimum of 6 characters",
        )

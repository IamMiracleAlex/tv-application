from django.contrib.auth.views import LogoutView
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users import views


class UserUrlsResolvesToViewTest(SimpleTestCase):
    def test_login_url_resolves_to_login_view(self):
        """assert that login url resolves to the login view class"""

        found = resolve(reverse("login"))
        self.assertEqual(found.func.view_class, views.CustomLoginView)

    def test_logout_url_resolves_to_logout_view(self):
        """assert that the logout url resolves to the logout view class"""

        found = resolve(reverse("logout"))
        self.assertEqual(found.func.view_class, LogoutView)

    def test_signup_url_resolves_to_register_view(self):
        """assert that the signup url resolves to the signup view"""

        found = resolve(reverse("signup"))
        self.assertEqual(found.func.view_class, views.SignupView)

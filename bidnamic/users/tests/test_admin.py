from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse

from users import admin
from users.models import User
from users.tests.factories import UserFactory


class UserAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user)

        # instantiate adminsite
        site = AdminSite()
        self.user_admin = admin.CustomUserAdmin(User, site)

    def test_changelist_view(self):
        """Assert user change list view loads well"""

        url = reverse(
            "admin:%s_%s_changelist"
            % (self.user._meta.app_label, self.user._meta.model_name)
        )
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        """Assert user change view page opens successfully"""

        url = reverse(
            "admin:%s_%s_change"
            % (self.user._meta.app_label, self.user._meta.model_name),
            args=(self.user.pk,),
        )
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

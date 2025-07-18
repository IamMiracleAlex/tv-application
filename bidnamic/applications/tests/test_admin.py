from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse

from applications import admin
from applications.models import Application
from applications.tests.factories import ApplicationFactory
from users.tests.factories import UserFactory


class ApplicationAdminTest(TestCase):
    def setUp(self):
        self.app = ApplicationFactory()
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user)

        # instantiate adminsite
        site = AdminSite()
        self.app_admin = admin.ApplicationAdmin(Application, site)

    def test_changelist_view(self):
        """Assert application change list view loads well"""

        url = reverse(
            "admin:%s_%s_changelist"
            % (self.app._meta.app_label, self.app._meta.model_name)
        )
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        """Assert application change view page opens successfully"""

        url = reverse(
            "admin:%s_%s_change"
            % (self.app._meta.app_label, self.app._meta.model_name),
            args=(self.app.pk,),
        )
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

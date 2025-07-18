from django.test import TestCase

from applications.models import Application
from applications.tests.factories import ApplicationFactory
from users.tests.factories import UserFactory


class ApplicationViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_index_page(self):
        """Assert index page loads"""

        url = "/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "applications/index.html")
        self.assertIn(b"Welcome To Bidnamic Multipart Form Wizard", resp.content)

    def test_create_application(self):
        """Assert create page loads and applications can be submitted"""

        url = "/create"
        self.client.force_login(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "applications/create_applications.html")
        self.assertIn(b"Submit An Application", resp.content)

        data = {
            "title": "Mr",
            "first_name": "Miracle",
            "surname": "Alex",
            "date_of_birth": "1995-03-30",
            "company_name": "bidnamic",
            "address": "lagos",
            "telephone": "0812233444",
            "bidding_settings": Application.HIGH,
            "google_account_ads_id": "1234567890",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/list")

    def test_list_page(self):
        """Assert application list page works"""

        # create applications
        url = "/list"
        apps = ApplicationFactory.create_batch(5)
        self.client.force_login(self.user)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "applications/list_applications.html")
        self.assertIn(apps[0].first_name, str(resp.content))

    def test_delete(self):
        """Assert delete action works"""

        app = ApplicationFactory()
        url = f"/{app.id}/delete"
        self.client.force_login(self.user)
        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/list")

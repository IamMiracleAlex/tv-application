from django.test import TestCase

from applications.tests.factories import ApplicationFactory


class ApplicationTest(TestCase):
    def test_model_creation(self):
        """Assert that the Application model was created properly"""

        app = ApplicationFactory()

        self.assertIsNotNone(app.title)
        self.assertIsNotNone(app.first_name)
        self.assertIsNotNone(app.surname)
        self.assertIsNotNone(app.date_of_birth)
        self.assertIsNotNone(app.company_name)
        self.assertIsNotNone(app.address)
        self.assertIsNotNone(app.telephone)
        self.assertIsNotNone(app.bidding_settings)
        self.assertIsNotNone(app.google_account_ads_id)

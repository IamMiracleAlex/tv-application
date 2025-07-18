from django.test import TestCase

from applications.forms import ApplicationForm
from applications.models import Application


class ApplicationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
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
        self.form_class = ApplicationForm

    def test_application_form(self):
        """
        Assert that form works as expected
        """

        form = self.form_class(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_birthdate_validity(self):
        """
        Assert birthdate must be up to 18 years
        """

        self.form_data["date_of_birth"] = "2020-03-22"
        form = self.form_class(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_of_birth"][0],
            "You must be 18 years old or older to fill this form",
        )

    def test_google_accounts_ads_id_validity(self):
        """
        Assert google accounts ads id must be 10 digits
        """

        self.form_data["google_account_ads_id"] = "123456789"
        form = self.form_class(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["google_account_ads_id"][0],
            "Google account ID must be 10 digits",
        )

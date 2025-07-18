from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from applications.models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": "2"}),
        }

    def clean_date_of_birth(self):
        birthdate = self.cleaned_data["date_of_birth"]
        today = date.today()
        # get age, difference between today and birthdate
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )
        if age < 18:
            raise ValidationError("You must be 18 years old or older to fill this form")

        return birthdate

    def clean_google_account_ads_id(self):
        google_account_ads_id = self.cleaned_data["google_account_ads_id"]
        if len(google_account_ads_id) != 10:
            raise ValidationError("Google account ID must be 10 digits")

        return google_account_ads_id

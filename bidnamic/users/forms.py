from django import forms
from django.utils.translation import ugettext_lazy as _

from users.models import User


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    error_messages = {
        "short_password": _("The password is too short, minimum of 6 characters"),
        "username_exists": _("This username is already registered"),
        "email_exists": _("This email address is already registered"),
        "password_mismatch": _("The password and password confirmation do not match"),
    }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username):
            raise forms.ValidationError(
                self.error_messages["username_exists"], code="username_exists"
            )
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                self.error_messages["email_exists"], code="email_exists"
            )
        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and len(password) < 6:
            raise forms.ValidationError(
                self.error_messages["short_password"],
                code="short_password",
            )
        if password != confirm_password:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password mismatch"
            )

        return self.cleaned_data

    def save(self):
        try:
            user = User.objects.create_user(
                username=self.cleaned_data.get("username"),
                email=self.cleaned_data.get("email"),
                password=self.cleaned_data.get("password"),
            )
            return user
        except Exception as e:
            raise ValueError(f"{str(e)}")

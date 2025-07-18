from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views import View

from users.forms import SignupForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Logs in a user"""

    template_name = "users/login.html"
    success_message = "Successfully logged in"


class SignupView(View):
    """Sign Up a new user"""

    template_name = "users/signup.html"
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Signup successful, please log in", extra_tags="success"
            )
            return redirect("login")

        messages.error(request, "Please correct the errors below", extra_tags="danger")
        return render(request, self.template_name, {"form": form})

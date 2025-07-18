from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic

from applications.forms import ApplicationForm
from applications.models import Application


class IndexView(generic.TemplateView):
    """Landing page view"""

    template_name = "applications/index.html"


class CreateView(LoginRequiredMixin, View):
    """Create an applicatiom"""

    login_url = "/login"
    redirect_field_name = "next"
    template_name = "applications/create_applications.html"
    form_class = ApplicationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Application submitted successfully", extra_tags="success"
            )
            return redirect("list")
        messages.error(request, "Please correct the errors below", extra_tags="danger")
        return render(request, self.template_name, {"form": form})


class ListView(View):
    """List all applications"""

    template_name = "applications/list_applications.html"
    paginate_by = 10

    def get(self, request):
        applications = Application.objects.all().order_by("-created_at")

        paginator = Paginator(applications, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            applications = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an intger deliver the first page
            applications = paginator.page(1)
        except EmptyPage:
            #  if page is out of range deliver last page of results
            applications = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {"applications": applications})


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    """Delete applications"""

    model = Application
    login_url = "/login"
    redirect_field_name = "next"
    success_url = reverse_lazy("list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        messages.success(
            request, "Application deleted successfully", extra_tags="success"
        )
        return response

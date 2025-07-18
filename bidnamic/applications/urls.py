from django.urls import path

from applications import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create", views.CreateView.as_view(), name="create"),
    path("list", views.ListView.as_view(), name="list"),
    path("<int:pk>/delete", views.DeleteView.as_view(), name="delete"),
]

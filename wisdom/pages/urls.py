from django.urls import path

from pages import views

urlpatterns = [
    path('', views.quotes, name='index'),
    path('quotes', views.quote_list, name='quotes'),
    path('quote/<int:id>', views.quote_detail, name='quote_detail'),
]
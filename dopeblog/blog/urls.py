from django.urls import path
from .views import index, detail, share, subscribe, search, about

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path("<int:year>/<int:month>/<int:day>/<slug:slug>/", detail, name='detail'),
    path('<int:post_id>/share/', share, name='share'),
    path('tag/<slug:tag_slug>/', index, name='posts_by_tag'),
    path('subscribe/', subscribe, name='subscribe'),
    path('search/', search, name='search'),
    path('about/', about, name='about')
    
]

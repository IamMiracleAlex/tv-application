from django.urls import path
from . import views
from django.conf.urls import url

from django.contrib.sitemaps import views as sitemap_views
from .sitemaps import MoviesSitemap, StaticSitemap

sitemaps = {'movies': MoviesSitemap, 'static': StaticSitemap}

urlpatterns = [
    path('', views.index, name='index'),
    path("home",  views.home_auth, name="home_auth"),
    path("explore/",views.explore, name = "explore"),
    path("explore/<int:id>",views.explore, name = "explore"),
    url(r"^explore/genre/$",views.genre, name = 'genre'),
    path("explore/genre/<str:new>/<int:id>",views.genre, name = 'genre'),
    path("explore/genre/<str:new>/",views.genre, name = 'genre'),
    path("movie/<int:id>/",  views.index_single, name="index_single"),
    path("movie/<int:pk>-<slug:slug>/",  views.single_movie, name="single_movie"),
    path("search",  views.search, name="search"),
    path("settings",  views.settings, name="settings"),
    path("series",  views.single_series, name="single_series"),
    path("donepages",  views.donepages, name="donepages"),
    path("signin",  views.signin, name="signin"),
    path("signup",  views.signup, name="signup"),
    path("profile",  views.profile, name="profile"),
    path("privacy",  views.privacy, name="privacy"),
    path("load",  views.loadmovies, name="loadmovies"),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

   path("add-watchlist",  views.add_watchlist, name="add_watchlist"),      
   path("play",  views.play, name="play"),      

]
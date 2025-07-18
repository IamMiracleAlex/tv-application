from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Movies
 
 
class MoviesSitemap(Sitemap):    
    changefreq = "never"
    priority = 0.9
 
    def items(self):
        return Movies.objects.all()



class StaticSitemap(Sitemap):
   priority = 0.6

   def items(self):
        return ['index', 'explore', 'home_auth', 'genre', 'privacy']

   def location(self, item):
        return reverse(item)



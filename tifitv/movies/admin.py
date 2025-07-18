from django.contrib import admin
from .models import Movies, Reactions, Usersettings, Comments, Watches, TmdbMovie
from django.contrib.sites.models import Site


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'genres', 'release_date', 'director', 'awards', 'country')
    list_per_page = 50
    search_fields = ('title',)
    list_filter = ('release_date', 'type')


admin.site.unregister(Site)

class SiteAdmin(admin.ModelAdmin): 
    list_display = ('id', 'domain', 'name') 
    
admin.site.register(Site, SiteAdmin)

admin.site.register(Reactions)
admin.site.register(Usersettings)
admin.site.register(Comments)


@admin.register(Watches)
class WatchesAdmin(admin.ModelAdmin):
    list_display = ('movieid', 'userid', 'status', 'created_at', 'updated_at')
    list_per_page = 50
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('userid',)
    raw_id_fields = ('movieid','userid')


@admin.register(TmdbMovie)
class TmdbMovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'revenue', 'status', 'imdb_id')
    list_per_page = 50


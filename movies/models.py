from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Movies(models.Model):
    movie_id = models.CharField(unique=True, max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    title = models.TextField()
    original_title = models.TextField(blank=True, null=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    runtime_minutes = models.FloatField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)
    num_imdb_ratings = models.IntegerField(blank=True, null=True)
    rated = models.TextField(blank=True, null=True) 
    release_date = models.DateTimeField(blank=True, null=True)
    primary_genre = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True) 
    plot = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True) 
    country = models.TextField(blank=True, null=True)  
    poster_url = models.CharField(max_length=2048, blank=True, null=True)
    rotten_tomatoes_score = models.FloatField(blank=True, null=True)
    metacritic_score = models.FloatField(blank=True, null=True)
    production = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=1024, blank=True, null=True)
    omdb_metascore = models.FloatField(blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    boxoffice_earnings = models.TextField(blank=True, null=True)
    writers = models.TextField(blank=True, null=True)
    dvd_release = models.DateTimeField(db_column='DVD_release', blank=True, null=True) 
    netflix_id = models.CharField(max_length=100, blank=True, null=True)
    amazon_id = models.CharField(max_length=100, blank=True, null=True)
    hulu_id = models.CharField(max_length=100, blank=True, null=True)
    total_seasons = models.IntegerField(blank=True, null=True)
    line_number = models.IntegerField(blank=True, null=True)
    cover_image = models.TextField(blank=True, null=True)
    url_slug = models.SlugField(unique = True,blank=True, null=True)
    main_trailer = models.CharField(max_length=2048, blank=True, null=True)
    reddit_url = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'movies'
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title
    
    def get_slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        url = reverse('single_movie', kwargs={'pk': self.pk, 'slug': self.get_slug()})
        return url

class TmdbMovie(models.Model):
    adult = models.BooleanField(default=False,null=True)
    backdrop_path = models.CharField(max_length=100, null=True)
    budget = models.IntegerField(null=True)
    genre = models.CharField(max_length=100,null=True)
    homepage = models.CharField(max_length=100,null=True)
    tmdb_id = models.IntegerField(null=True)
    imdb_id = models.CharField(max_length=100,null=True)
    original_title = models.CharField(max_length=100, null=True)
    overview = models.TextField(null=True)
    popularity = models.IntegerField(null=True)
    poster_path = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=100, null=True)
    revenue = models.CharField(max_length=100, null=True)
    runtime = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    tagline = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    video = models.BooleanField(null=True)
    vote_average = models.IntegerField(null=True)
    vote_count = models.IntegerField(null=True)
    

    class Meta:
        verbose_name_plural = "TMDB Movies"

    def __str__(self):
        return self.title
   



class Usersettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    personalitytype = models.TextField(db_column='personalityType', blank=True, null=True)  # Field name made lowercase.
    genres = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    dateofbirth = models.DateField(db_column='dateOfBirth', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(db_column='timeZone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dateformat = models.CharField(db_column='dateFormat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timeformat = models.CharField(db_column='timeFormat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    weekstarts = models.CharField(db_column='weekStarts', max_length=255, blank=True, null=True)  # Field name made lowercase.
    services = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'usersettings'
        verbose_name_plural = "User Settings"

    def __str__(self):
        return self.created_at


class Watches(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.DO_NOTHING, db_column='movieId')  # Field name made lowercase.
    status = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True)

    class Meta:
        db_table = 'watches'
        verbose_name_plural = 'Watches'


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.CASCADE, db_column='movieId')  # Field name made lowercase.
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='replies')
    type = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'comments'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comments


class Reactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.DO_NOTHING, db_column='movieId')  # Field name made lowercase.
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'reactions'
        verbose_name_plural = ' Reactions'

    def __str__(self):
        return self.type    



class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)    
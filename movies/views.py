from django.shortcuts import render, get_object_or_404, redirect
from .models import Movies, Watches, TmdbMovie, Reactions
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.http import QueryDict, HttpResponse, JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import requests
import json


def index(request):
    movies = TmdbMovie.objects.all().order_by('-popularity')[:24]
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)


def index_single(request, id):
    single = get_object_or_404(TmdbMovie, id=id)

    try:
        movies = Movies.objects.filter(movie_id=single.imdb_id)
        for movie in movies:
            return redirect('single_movie', pk=movie.id, slug=slugify(movie.title))
    except:
        pass
    return redirect('index')


@login_required(login_url='/signin-email')
def home_auth(request):
    movies = Movies.objects.all().order_by('-num_imdb_ratings')
    paginator = Paginator(movies, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except(EmptyPage, InvalidPage):
        movies = paginator.page(page)
    return render(request, 'movies/home_auth.html', {'movies': movies})


def explore(request, id=None):
    if id is None:
        id = 1
    movies = Movies.objects.all().order_by('-num_imdb_ratings')
    paginator = Paginator(movies, 20)
    try:
        page = int(id)
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except(EmptyPage, InvalidPage):
        movies = paginator.page(page)
    return render(request, 'movies/explore.html', {'movies': movies})


def genre(request, new=None, id=None):
    if id is None:
        id = 1
    context_dict = {}
    if request.is_ajax():
        if request.method == 'GET':
            if 'search-persons-post' in request.session:
                request.POST = QueryDict('').copy()
                request.POST.update(request.session['search-persons-post'])
                request.method = 'POST'

        if request.method == 'POST':
            request.session['search-persons-post'] = request.POST
            checkbox_selected = request.POST.getlist('genre[]')
            query = Q()
            for selected in checkbox_selected:
                query = query | Q(genres=selected)
            filtered_genre = Movies.objects.filter(query)
            movies = filtered_genre.all().order_by('-num_imdb_ratings')

        paginator = Paginator(movies, 20)
        try:
            page = int(id)
        except PageNotAnInteger:
            page = 1
        try:
            movies = paginator.page(page)
        except(EmptyPage, InvalidPage):
            movies = paginator.page(page)
        context_dict['movies'] = movies
        return render(request, 'movies/movie_listing.html', context_dict)
    else:
        if 'and' in new:
            genre_list = new.split('-and-')
        else:
            genre_list = [new]
        query = Q()
        for selected in genre_list:
            query = query | Q(genres=selected)
        filtered_genre = Movies.objects.filter(query)
        movies = filtered_genre.all().order_by('-num_imdb_ratings')
        paginator = Paginator(movies, 20)
        try:
            page = int(id)
        except PageNotAnInteger:
            page = 1
        try:
            movies = paginator.page(page)
        except(EmptyPage, InvalidPage):
            movies = paginator.page(page)
        context_dict['movies'] = movies
        return render(request, 'movies/explore.html', context_dict)


def single_movie(request, pk, slug):
    context, watches,reactions = {}, None,None
    movie = Movies.objects.filter(pk=pk, url_slug=slug)
    if len(movie) == 0:
        movie = Movies.objects.filter(pk=pk)
        if request.user.is_authenticated:
            
            try:
                watches = Watches.objects.filter(
                    movieid=movie[0]).filter(userid=request.user)
            except Exception as e:
                pass
            
        else:
            watches = ['']
    if request.user.is_authenticated:
        try:
            reactions = Reactions.objects.get(userid=request.user,movieid=movie[0])
        except Exception:
            pass

    context = {"movie": movie[0], 'watches': watches,'reactions':reactions}
    return render(request, 'movies/single_movie.html', context)


def add_watchlist(request):
    final_status, auth = None, None
    if request.user.is_authenticated:

        movie_id = request.GET.get('movie_id', None)
        movie = Movies.objects.get(pk=movie_id)
        watched = Watches.objects.filter(
            movieid=movie).filter(userid=request.user).exists()

        if watched:
            watch = Watches.objects.get(movieid=movie, userid=request.user)
            watch.status = not watch.status
            final_status = watch.status
            watch.save()

        else:
            watch = Watches(movieid=movie, userid=request.user, status=True)
            watch.save()
            final_status = True

    else:
        auth = "Please login to add movies to your watch list"

    data = {'final_status': final_status, 'auth': auth}

    return JsonResponse(data)


def seen(request):
    if request.user.is_authenticated:
        movie_id = request.GET.get('movie_id', None)
        movie = Movies.objects.get(pk=movie_id)
        seen = Reactions.objects.filter(
            movieid=movie).filter(userid=request.user).exists()
        if seen:
            seen_before = Reactions.objects.get(movieid=movie, userid=request.user)
        else:
            seen_before = Reactions(movieid=movie, userid=request.user)
            seen_before.save()
        data ={'status':True}
    return JsonResponse(data)

def search(request):
    query = None
    results = []
    paged_results = None

    if 'q' in request.GET:
        query = request.GET['q']
        results = Movies.objects.filter(title__search=query).filter(
            poster_url__isnull=False).exclude(poster_url='N/A').order_by('-num_imdb_ratings')

        paginator = Paginator(results, 20)
        page = request.GET.get('page')
        try:
            paged_results = paginator.page(page)
        except PageNotAnInteger:
            paged_results = paginator.page(1)
        except EmptyPage:
            paged_results = paginator.page(paginator.num_pages)

    return render(request, 'movies/search.html', {'results': paged_results,
                                                  'paginator': paginator, 'query': query})


@login_required(login_url='/signin-email')
def settings(request):
    return render(request, 'movies/settings.html')


def single_series(request):
    return render(request, 'movies/single_series.html')


def donepages(request):
    return render(request, 'movies/donepages.html')


def signup(request):
    return render(request, 'account/signup_noemail.html')


def signin(request):
    return render(request, 'account/signin.html')


def profile(request):
    return render(request, 'movies/profile.html')


def privacy(request):
    return render(request, 'movies/privacy.html')


def loadmovies(request):
    movie_ids = []
    error = None

    for i in range(1, 3):

        res = requests.get(
            f'https://api.themoviedb.org/3/movie/popular?api_key=f4c312fa36258f9c7cd5554863b7254b&page={i}').json()

        for r in res['results']:
            movie_ids.append(r['id'])

    for movie_id in movie_ids:
        resp = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f4c312fa36258f9c7cd5554863b7254b').json()
        try:
            obj, created = TmdbMovie.objects.update_or_create(adult=resp['adult'], backdrop_path=f"https://image.tmdb.org/t/p/w500{resp['backdrop_path']}", budget=resp['budget'], genre=resp['genres'][0]['name'], homepage=resp['homepage'], tmdb_id=resp['id'], imdb_id=resp['imdb_id'], original_title=resp['original_title'], overview=resp['overview'], popularity=resp['popularity'], poster_path=f"https://image.tmdb.org/t/p/w500{resp['poster_path']}", release_date=resp['release_date'], revenue=resp['revenue'], runtime=resp['runtime'], status=resp['status'], tagline=resp['tagline'], title=resp['title'], video=resp['video'], vote_average=resp['vote_average'], vote_count=resp['vote_count'])

        except Exception as e:
            error = f'The following error occured: {e}'

    context = {'error': error, 'success': 'Movies was loaded successfully!'}

    return render(request, 'movies/loadmovies.html', context)


# for testing pages

def play(request):
    return render(request, 'movies/donepages.html')

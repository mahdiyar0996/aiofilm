from django.shortcuts import render, redirect
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from products.models import Category, Genre, Movie, Years
from datetime import datetime, date
from django.db.models import Count
from config.settings import redis
from django.core.cache import cache
from .templatetags.filters import order_by_merge_sort
from .decorators import debugger


class Home(View):
    @debugger
    def get(self, request):
        user = redis.hget(f"user-{request.session.get('_auth_user_id')}", 'id')
        if not user and request.session.get('_auth_user_id'):
            user = request.user
            with redis.pipeline() as pipeline:
                pipeline.hset(f"user-{request.session.get('_auth_user_id')}", mapping=request.user.to_dict())
                pipeline.expire(f"user-{request.session.get('_auth_user_id')}", 60 * 30)
                pipeline.execute()

        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all().values('id', 'title', 'slug')
            cache.set('categories', categories, 60 * 180)

        genres = cache.get('categories-genres')
        if not genres:
            category_name = []
            for item in categories:
                category_name.append(item['title'])
            genres = Genre.objects.prefetch_related('movie__category')\
            .filter(movie__category__title__in=category_name).values('movie__category', 'title').distinct()
            cache.set('categories-genres', genres, 60 * 120)
            
        years = cache.get('categories-years')
        if not years:
            years = Years.objects.prefetch_related('movie__category').all().distinct().values('movie__category', 'year')
            cache.set('categories-years', years, 60 * 120)
        
        movies = cache.get('random-movies')
        if not movies:
            movies = Movie.objects.select_related('category', 'year').prefetch_related('favorite').\
            annotate(favorite_count=Count('favorite')).all().values('year__year', 'image',
                                                                     'name', 'imdb_rate',
                                                                     'age_limit', 'is_ongoing',
                                                                     'language', 'created_at','favorite_count',
                                                                     'category__slug').order_by('?')[:50]            
            cache.set('random-movies', movies, 60 * 1)

        context = {'genres': genres,
                   'years': years,
                   'movies': movies,
                   'user': user,
                   'categories': categories}
        return render(request, 'home.html', context)
        

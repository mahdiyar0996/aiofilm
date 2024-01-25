from django.shortcuts import render, redirect
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from products.models import Category, Genre, Movie, Years
from datetime import datetime, date
# def binary_search(query):
#     years = []
#     for item in query:
#         high = len(item) - 1
#         low = 0
#         while low <= high:
#             mid = high // 2
#             year = item['movie__release_at']
#             if year 

class Home(View):
    def get(self, request):
        categories = Category.objects.prefetch_related('movie').all().values('id', 'title', 'slug')
        category_name = []
        for item in categories:
            category_name.append(item['title'])
            
        genres = Genre.objects.prefetch_related('movie__category').filter(movie__category__title__in=category_name).values('movie__category', 'title').distinct()
        years = Years.objects.prefetch_related('movie__category').all().distinct().values('movie__category', 'year')
        movies = Movie.objects.select_related('category', 'year').all().values('year__year', 'image', 'name', 'imdb_rate',
                                            'age_limit', 'is_ongoing', 'language',
                                            'category').order_by('?')
        context = {'genres': genres,
                   'years': years,
                   'movies': movies,
                   'categories': categories}
        print(dir(request))
        return render(request,'home.html', context)
        

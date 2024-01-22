from django.contrib import admin
from .models import Movie, Category, Genre, Season, Episode


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ['category', 'genre', 'season']}),
        ('جزعیات', {'fields': ['image', 'name', 'persian_name', 'ongoing_day']}),
        ('جزعیات', {'fields': ['is_ongoing', 'is_active']}),
        ('جزعیات', {'fields': ['average_time', 'product_of', 'quality', 'imdb_rate', 'age_limit']}),
        ('جزعیات', {'fields': ['director', 'super_stars', 'translation_team', 'translator']}),
        ('جزعیات', {'fields': ['release_at', 'created_at', 'updated_at']})
    )
    readonly_fields = ['created_at', 'updated_at']
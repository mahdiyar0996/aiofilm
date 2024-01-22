from django.contrib import admin
from .models import Movie, Category, Genre, Season, Episode


# @admin.register(Category)
# class MovieAdmin(admin.ModelAdmin):
#     fields = ['title']
    
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ['category', 'genre', 'season']}),
        ('', {'fields': ['image', 'name', 'persian_name', 'summary', 'ongoing_day']}),
        ('', {'fields': ['is_ongoing', 'is_active']}),
        ('', {'fields': ['average_time', 'product_of', 'quality', 'imdb_rate', 'age_limit']}),
        ('', {'fields': ['director', 'super_stars', 'translation_team', 'translator']}),
        ('', {'fields': ['release_at', 'created_at', 'updated_at']})
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'name', 'persian_name', 'is_active', "imdb_rate",
                    'is_ongoing', 'created_at', 'updated_at']
    list_display_links = ['id', 'name', 'persian_name']
    list_per_page = 100
    list_filter = ['category', 'genre', 'season', 'is_active', 'is_ongoing', 'quality', 'product_of']
    search_fields = ['name', 'persian_name']
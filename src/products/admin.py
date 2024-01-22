from django.contrib import admin
from .models import Movie, Category, Serial, Genre, Season, Episode


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['title', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_display = ['id','title', 'created_at', 'updated_at']

class SerialAdmin(admin.StackedInline):
    model = Serial
    fields = ['movie', 'season']
    readonly_fields = ['created_at', 'updated_at']
    extra = 0

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    fields = ['season_number', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display_links = ['id', 'season_number']
    list_display = ['id','season_number', 'created_at', 'updated_at']


class SeasonAdmin(admin.StackedInline):
    model = Season
    fields = ['season_number']
    readonly_fields = ['created_at', 'updated_at']


class EpisodeAdmin(admin.StackedInline):
    model = Episode
    fields = ['movie', 'season', 'file']
    readonly_fields = ['created_at', 'updated_at']
    extra = 0

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ['image', 'name', 'persian_name']}),
        ('', {'fields': ['category', 'genre']}),
        ('', {'fields': ['is_ongoing', 'is_active' , 'summary']}),
        ('', {'fields': ['ongoing_day', 'average_time', 'product_of','anime_type', 'quality', 'imdb_rate', 'age_limit']}),
        ('', {'fields': ['director', 'super_stars', 'translation_team', 'translator']}),
        ('', {'fields': ['release_at', 'created_at', 'updated_at']})
    )
    filter_horizontal = ('genre',)
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id', 'name', 'persian_name', 'is_active', "imdb_rate",
                    'is_ongoing', 'created_at', 'updated_at']
    list_display_links = ['id', 'name', 'persian_name']
    list_per_page = 100
    list_filter = ['category', 'genre', 'is_active', 'is_ongoing', 'quality', 'product_of']
    search_fields = ['name', 'persian_name']
    inlines = [SerialAdmin, EpisodeAdmin]
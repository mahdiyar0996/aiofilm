from django.contrib import admin
from .models import Movie, Category, Serial, Genre, Season, Episode, Years


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'created_at', 'updated_at']
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
    fields = ['season_number','language', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display_links = ['id', 'season_number']
    list_display = ['id','season_number', 'created_at', 'updated_at']


class SeasonAdmin(admin.StackedInline):
    model = Season
    fields = ['season_number', 'language']
    readonly_fields = ['created_at', 'updated_at']
    
    
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    fields = ['movie', 'season', 'file', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['id','movie', 'season', 'file']
    list_display_links = ['id', 'movie', 'season', 'file']
    search_fields = ['movie',]
    list_per_page = 100

class EpisodeAdmin(admin.StackedInline):
    model = Episode
    fields = ['movie', 'season', 'file']
    readonly_fields = ['created_at', 'updated_at']
    extra = 0

@admin.register(Years)
class YearAdmin(admin.ModelAdmin):
    fields = ['year']
    list_display = ['id', 'year']
    list_display_links = ['id', 'year']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ['image', 'name', 'persian_name']}),
        ('', {'fields': ['category', 'genre']}),
        ('', {'fields': ['is_ongoing', 'is_active' , 'summary']}),
        ('', {'fields': ['ongoing_day', 'average_time', 'language', 'product_of','anime_type', 'quality', 'imdb_rate', 'age_limit']}),
        ('', {'fields': ['director', 'super_stars', 'translation_team', 'translator']}),
        ('', {'fields': ['year', 'release_at', 'created_at', 'updated_at']})
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
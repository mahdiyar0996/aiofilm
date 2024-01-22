from django.db import models
from django.db.models import F, Q
from django_jalali.db import models as jmodels


class AbstractBase(models.Model):
    updated_at = jmodels.jDateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = jmodels.jDateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True)
    
    def active_users(self):
        return self.objects.filter(is_active=True)
    
    class Meta:
        abstract = True
     
        
class Category(AbstractBase):
    title = models.CharField('عنوان', max_length=64)
     
    class Meta:
        db_table = 'Category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
 
 
class Season(AbstractBase):
    season_number = models.SmallIntegerField('فصل', db_index=True)
     
    class Meta:
        db_table = 'Season'
        verbose_name = 'season'
        verbose_name_plural = 'seasons'
        
        
class Episode(AbstractBase):
    movie = models.ForeignKey('Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    season = models.ForeignKey(Season, verbose_name='فصل', related_name='%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField('فایل', upload_to='media/product/files')
 
    class Meta:
        db_table = 'Episode'
        verbose_name = 'episode'
        verbose_name_plural = 'episodes'
        
    def __str__(self):
        return self.movie.name
 
 
class Genre(AbstractBase):
    title = models.CharField('عنوان', max_length=62)
    
    class Meta:
        db_table = 'Genres'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        
    def __str__(self):
        return self.title


class Movie(AbstractBase):
    qualities = [
        ('WEB-DL', 'WEB-DL'),
        ('HDTV', 'HDTV'),
        ('BluRay', 'BluRay')
    ]
    movie_type = [
        ('سریال', 'series'),
        ('فیلم', 'movie')
    ]
    ongoing_days = [
        ('شنبه', 1),
        ('یکشنبه', 2),
        ('دوشنبه', 3),
        ('سه شنبه', 4),
        ('چهارشنبه', 5),
        ('پنجشنبه', 6),
        ('جمعه', 7),
    ]
    category = models.ForeignKey(Category, verbose_name="مجموعه", related_name='%(class)s', db_index=True, on_delete=models.DO_NOTHING)
    genre = models.ManyToManyField(Genre, verbose_name="ژانر", related_name='%(class)s', db_index=True)
    season = models.ManyToManyField(Season, verbose_name="فصل", related_name='%(class)s')
    image = models.ImageField('عکس', upload_to='media/product/images/')
    name = models.CharField('نام', max_length=252)
    persian_name = models.CharField('نام فارسی', max_length=252)
    average_time = models.SmallIntegerField("مدت زمان", blank=True, null=True)
    product_of = models.CharField('محصول', max_length=64, blank=True, null=True)
    quality = models.CharField('کیفیت نمایش', max_length=64, choices=qualities, blank=True, null=True)
    imdb_rate = models.PositiveSmallIntegerField('رتبه imdb')
    age_limit = models.SmallIntegerField('محدوده سنی', default=13)
    director = models.CharField("کارگردان", max_length=64, blank=True, null=True)
    super_stars = models.CharField('ستارگان', max_length=252, blank=True, null=True)
    is_ongoing = models.BooleanField('وضعیت پخش', db_default=False)
    ongoing_day = models.PositiveSmallIntegerField('روز پخش', choices=ongoing_days, db_default=False)
    release_at = models.DateField('پخش از', blank=True, null=True)
    translation_team = models.CharField('تیم ترجمه',max_length=64, blank=True, null=True)
    translator = models.CharField('مترجم', max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'Movie'
        verbose_name = 'movie'
        verbose_name_plural = 'movies'
        
    def __str__(self):
        return self.title
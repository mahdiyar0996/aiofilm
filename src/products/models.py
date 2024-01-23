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
    title = models.CharField('عنوان', max_length=64, null=True)
     
    class Meta:
        db_table = 'Category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
          
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
        (1, 'شنبه'),
        (2, "یکشنبه"),
        (3, "دوشنبه"),
        (4, "چهارشنبه"),
        (5, "پنجشنبه"),
        (6, 'جمعه'),
    ]
    anime_type = (
        ('سینمایی', 'movie'),
        ('سریالی', 'series'),
        ('ova', 'ova'),
    )
    category = models.ForeignKey(Category, verbose_name="مجموعه", related_name='%(class)s', db_index=True, on_delete=models.DO_NOTHING)
    genre = models.ManyToManyField('Genre', verbose_name="ژانر", related_name='%(class)s', db_index=True)
    image = models.ImageField('عکس', upload_to='media/product/images/')
    name = models.CharField('نام', max_length=252)
    persian_name = models.CharField('نام فارسی', max_length=252)
    summary = models.TextField('خلاصه', blank=True, null=True)
    average_time = models.SmallIntegerField("مدت زمان", blank=True, null=True)
    product_of = models.CharField('محصول', max_length=64, blank=True, null=True)
    anime_type = models.CharField('نوع انیمه', max_length=64, choices=anime_type, blank=True, null=True)
    quality = models.CharField('کیفیت نمایش', max_length=64, choices=qualities, blank=True, null=True)
    imdb_rate = models.FloatField('رتبه imdb')
    age_limit = models.SmallIntegerField('محدوده سنی', default=13)
    director = models.CharField("کارگردان", max_length=64, blank=True, null=True)
    super_stars = models.CharField('ستارگان', max_length=252, blank=True, null=True)
    is_ongoing = models.BooleanField('در حال پخش', db_default=False)
    ongoing_day = models.PositiveSmallIntegerField('روز پخش', choices=ongoing_days, db_default=False)
    release_at = models.DateField('پخش از', blank=True, null=True)
    translation_team = models.CharField('تیم ترجمه',max_length=64, blank=True, null=True)
    translator = models.CharField('مترجم', max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'Movie'
        verbose_name = 'movie'
        verbose_name_plural = 'movies'
        
    def __str__(self):
        return self.name

class Genre(AbstractBase):
    title = models.CharField('عنوان', max_length=62)
    
    class Meta:
        db_table = 'Genres'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        
    def __str__(self):
        return self.title


class Serial(AbstractBase):
    movie =  models.ForeignKey(Movie, verbose_name=("فیلم"),related_name="%(class)s", on_delete=models.DO_NOTHING)
    season = models.ForeignKey('Season', verbose_name='فصل', related_name="%(class)s", on_delete=models.DO_NOTHING)
    is_active = None
    class Meta:
        db_table = 'Serial'
        verbose_name = 'serial'
        verbose_name_plural = 'series'
        
    def __str__(self):
        return self.movie.name
 
class Season(AbstractBase):
    season_number = models.SmallIntegerField('فصل', db_index=True)
    is_active = None
    class Meta:
        db_table = 'Season'
        verbose_name = 'season'
        verbose_name_plural = 'seasons'
        
    def __str__(self):
        return f"فصل {self.season_number}"
        
        
class Episode(AbstractBase):
    movie = models.ForeignKey('Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    season = models.ForeignKey(Season, verbose_name='فصل', related_name='%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField('فایل', upload_to='media/product/files')
    is_active = None
 
    class Meta:
        db_table = 'Episode'
        verbose_name = 'episode'
        verbose_name_plural = 'episodes'
        ordering = ['file', ]
        
    def __str__(self):
        return self.movie.name
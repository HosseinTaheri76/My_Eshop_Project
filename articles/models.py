from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from utilties.models import slugify
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from .uploaders import article_image_uploader

# Create your models here.
_User = get_user_model()


class Category(MPTTModel):
    fa_name = models.CharField(
        max_length=75,
        unique=True,
        verbose_name='نام دسته بندی فارسی',
    )
    en_name = models.CharField(
        max_length=75,
        unique=True,
        verbose_name='نام دسته بندی انگیلیسی',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='زیر شاخه ی'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='اسلاگ',
        help_text='نام دسته بندی انگیلیسی را وارد کنید به جای فاصله از آندرلاین استفاده کنید.'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.en_name)
        super().save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['en_name']

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def _get_name_path(self, lang_name='en_name'):
        category_names = [getattr(self, lang_name)]
        node = self
        while node.parent:
            node = node.parent
            category_names.append(getattr(node, lang_name))
        return ' / '.join(category_names[::-1])

    def __str__(self):
        return self._get_name_path(lang_name='fa_name')

    def get_related_articles(self):
        return Article.objects.filter(category__in=self.get_descendants(include_self=True)).order_by('-id')

    def get_absolute_url(self):
        return reverse('articles_by_category', args=(self.slug,))


class ArticleTag(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام برچسب', unique=True)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='اسلاگ',
        help_text='نام برچسب را وارد کنید به جای فاصله از آندرلاین استفاده کنید.'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'


class Article(models.Model):
    author = models.ForeignKey(_User, on_delete=models.CASCADE, related_name='articles', verbose_name='نویسنده')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='دسته بندی')
    image = models.ImageField(upload_to=article_image_uploader, verbose_name='عکس اصلی خبر')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    body = RichTextUploadingField(verbose_name='بدنه مقاله', config_name='advanced')
    date_published = models.DateField(auto_now_add=True, verbose_name='تاریخ انتشار')
    tags = models.ManyToManyField(ArticleTag, blank=True, verbose_name='برچسب ها')
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='اسلاگ',
        help_text='نام برچسب را وارد کنید به جای فاصله از آندرلاین استفاده کنید.'
    )
    view_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')

    def increase_visited(self):
        self.view_count += 1
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=(self.id, self.slug))
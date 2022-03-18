from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from model_utils import FieldTracker
from . import uploaders
from ckeditor.fields import RichTextField
from utilties.models import slugify
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core import validators


class ProductManager(models.Manager):
    def search(self, category, product_name):
        name_lookup = Q(fa_name__icontains=product_name) | Q(en_name__icontains=product_name)
        if category.isdigit():
            base_query = self.get_queryset().filter(
                category__in=get_object_or_404(Category, id=int(category)).get_descendants(include_self=True)
            )
        else:
            base_query = self.get_queryset()
        return base_query.filter(name_lookup).order_by('-id')


class DefaultSpecificationValue(models.Model):
    specification = models.ForeignKey(
        'ProductSpecifications',
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name='مشخصه'
    )
    value = models.CharField(max_length=75, verbose_name='مقدار مشخصه')

    def __str__(self):
        return f'{self.specification} : {self.value}'

    class Meta:
        verbose_name = 'مقدار مشخصه'
        verbose_name_plural = 'مقادیر پیش فرض مشخصه'


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

    def get_type_root(self):
        current = self
        while not current.specifications.count():
            current = current.parent
            if not current:
                return []
        return current.id, current.specifications.all()

    def get_specs(self):
        return self.get_type_root()[1] if self.get_type_root() else []

    def search_fields(self):
        searchable_attrs = [attr for attr in self.get_specs() if attr.is_searchable()]
        return {attr: attr.values.all() for attr in searchable_attrs}

    def related_products(self):
        return Product.objects.filter(category__in=self.get_descendants(include_self=True)).order_by('-id')

    def get_absolute_url(self):
        return reverse('products_category', args=(self.slug,))


class ProductBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام برند', unique=True)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='اسلاگ',
        help_text='نام برند را وارد کنید به جای فاصله از آندرلاین استفاده کنید.'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class ProductTag(models.Model):
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

    def get_related_products(self):
        return self.product_set.all()


class ProductSpecifications(models.Model):
    name = models.CharField(max_length=50, verbose_name='مشخصه')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='specifications')

    class Meta:
        unique_together = ('name', 'category')
        verbose_name = 'مشخصه'
        verbose_name_plural = 'مشخصات'

    def __str__(self):
        return self.name

    def is_searchable(self):
        return bool(self.values.count())


class Product(models.Model):
    en_name = models.CharField(
        max_length=150,
        verbose_name='نام محصول انگیلیسی',
        unique=True
    )
    fa_name = models.CharField(
        max_length=150,
        verbose_name='نام فارسی محصول',
        unique=True,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='اسلاگ',
        help_text='نام محصول انگیلیسی را وارد کنید به جای فاصله از آندرلاین استفاده کنید.'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'children': None},
        verbose_name='دسته بندی محصول'
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='برند محصول'
    )
    base_price = models.PositiveBigIntegerField(verbose_name='قیمت پایه محصول به تومان')
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[validators.MaxValueValidator(99, 'درصد تخفیف نمی تواند از 99 درصد پیشتر یاشد.')],
        verbose_name='درصد تخفیف',
    )
    stock = models.PositiveIntegerField(default=10, null=True, blank=True, verbose_name='تعداد موجودی')
    user_favorites = models.ManyToManyField(
        get_user_model(),
        related_name='favorite_products',
        verbose_name='علاقه مندی کاربران'
    )

    description = RichTextField(
        verbose_name='توضیح کوتاه',
        config_name='basic',
        max_length='300'
    )
    image = models.ImageField(
        max_length=1000,
        upload_to=uploaders.product_img_uploader,
        verbose_name='عکس اصلی محصول'
    )
    product_tags = models.ManyToManyField(
        ProductTag,
        blank=True,
        verbose_name='برچسب ها'
    )

    times_visited = models.PositiveIntegerField(verbose_name='تعداد بازدید', default=0)
    date_created = models.DateTimeField(verbose_name='تاریخ ایجاد محصول', auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name='تاریخ ویرایش محصول', auto_now=True)
    number_sold = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')

    objects = ProductManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fa_name or self.en_name)
        super().save(*args, **kwargs)

    def increase_visited(self):
        self.times_visited += 1
        self.save()

    tracker = FieldTracker(fields=['category', 'stock', 'discount_percent'])

    def __str__(self):
        return self.fa_name or self.en_name

    @property
    def is_available(self):
        return self.stock > 0

    @property
    def title(self):
        return self.fa_name or self.en_name

    @property
    def price(self):
        try:
            return int(self.base_price * (1 - (self.discount_percent / 100)))
        except TypeError:
            return '-'

    @property
    def is_discounted(self):
        return self.discount_percent > 0

    @property
    def root_category(self):
        return self.category.get_type_root()[0]

    @staticmethod
    def make_compare_ready(*args):
        assert len(set(product.root_category for product in args)) == 1, 'products do not belong to same type'
        attrs = ['تصویر محصول', 'عنوان'] + [spec.specification.name for spec in args[0].specifications.all()]
        values = []
        for product in args:
            values.append(
                [mark_safe(f'<img src="{product.image.url}" alt="">'), product.title] + [spec.value for spec in
                                                                                         product.specifications.all()])
        return list(zip(attrs, *values))

    def get_absolute_url(self):
        return reverse('product_detail', args=(self.id, self.slug))

    def buy(self, qty):
        self.number_sold += qty
        self.stock -= qty
        self.save()

    def add_user_to_favorites(self, user):
        if user not in self.user_favorites.all():
            self.user_favorites.add(user)
            return True
        return False

    def delete_from_user_favorites(self, user):
        if self in user.favorite_products.all():
            user.favorite_products.remove(self)
            return True
        return False

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductSpecificationValue(models.Model):
    specification = models.ForeignKey(ProductSpecifications, on_delete=models.CASCADE, verbose_name='مشخصه')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    value = models.CharField(max_length=75, default='وارد نشده', verbose_name='مقدار مشخصه')

    def __str__(self):
        return ''

    class Meta:
        unique_together = ('specification', 'product')
        verbose_name_plural = 'مشخصات محصول'


class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(
        upload_to=uploaders.product_gallery_uploader,
        verbose_name='فایل تصویر محصول',
        unique=True,
        max_length=1000,
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = 'گالری تصاویر محصول'


class ProductCollection(models.Model):
    categories = models.ManyToManyField(
        Category,
        symmetrical=False,
        limit_choices_to={'children': None},
        verbose_name='دسته بندی ها',
        related_name='categories'
    )
    name = models.CharField(max_length=100, verbose_name='نام کلکسیون', unique=True)
    cover_image = models.ImageField(upload_to=uploaders.collection_cover_uploader, verbose_name='عکس کاور')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('products_collection', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProductCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

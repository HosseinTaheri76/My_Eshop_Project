# Generated by Django 3.2.8 on 2022-01-08 04:04

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import products.uploaders


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fa_name', models.CharField(max_length=75, unique=True, verbose_name='نام دسته بندی فارسی')),
                ('en_name', models.CharField(max_length=75, unique=True, verbose_name='نام دسته بندی انگیلیسی')),
                ('slug', models.SlugField(help_text='نام دسته بندی انگیلیسی را وارد کنید به جای فاصله از آندرلاین استفاده کنید.', max_length=100, unique=True, verbose_name='اسلاگ')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='زیر شاخه ی')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_name', models.CharField(max_length=150, unique=True, verbose_name='نام محصول انگیلیسی')),
                ('fa_name', models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='نام فارسی محصول')),
                ('slug', models.SlugField(help_text='نام محصول انگیلیسی را وارد کنید به جای فاصله از آندرلاین استفاده کنید.', max_length=150, unique=True, verbose_name='اسلاگ')),
                ('base_price', models.PositiveBigIntegerField(verbose_name='قیمت پایه محصول به تومان')),
                ('discount_percent', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99, 'درصد تخفیف نمی تواند از 99 درصد پیشتر یاشد.')], verbose_name='درصد تخفیف')),
                ('stock', models.PositiveIntegerField(blank=True, default=10, null=True, verbose_name='تعداد موجودی')),
                ('description', ckeditor.fields.RichTextField(max_length='300', verbose_name='توضیح کوتاه')),
                ('image', models.ImageField(max_length=1000, upload_to=products.uploaders.product_img_uploader, verbose_name='عکس اصلی محصول')),
                ('times_visited', models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد محصول')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش محصول')),
                ('number_sold', models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام برند')),
                ('slug', models.SlugField(help_text='نام برند را وارد کنید به جای فاصله از آندرلاین استفاده کنید.', max_length=100, unique=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='مشخصه')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='products.category')),
            ],
            options={
                'verbose_name': 'مشخصه',
                'verbose_name_plural': 'مشخصات',
                'unique_together': {('name', 'category')},
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام برچسب')),
                ('slug', models.SlugField(help_text='نام برچسب را وارد کنید به جای فاصله از آندرلاین استفاده کنید.', max_length=100, unique=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
        migrations.CreateModel(
            name='ProductImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(max_length=1000, unique=True, upload_to=products.uploaders.product_gallery_uploader, verbose_name='فایل تصویر محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'verbose_name_plural': 'گالری تصاویر محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام کلکسیون')),
                ('cover_image', models.ImageField(upload_to=products.uploaders.collection_cover_uploader, verbose_name='عکس کاور')),
                ('slug', models.SlugField(unique=True)),
                ('categories', models.ManyToManyField(limit_choices_to={'children': None}, related_name='categories', to='products.Category', verbose_name='دسته بندی ها')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productbrand', verbose_name='برند محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(limit_choices_to={'children': None}, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category', verbose_name='دسته بندی محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_tags',
            field=models.ManyToManyField(blank=True, to='products.ProductTag', verbose_name='برچسب ها'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_favorites',
            field=models.ManyToManyField(related_name='favorite_products', to=settings.AUTH_USER_MODEL, verbose_name='علاقه مندی کاربران'),
        ),
        migrations.CreateModel(
            name='DefaultSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=75, verbose_name='مقدار مشخصه')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='products.productspecifications', verbose_name='مشخصه')),
            ],
            options={
                'verbose_name': 'مقدار مشخصه',
                'verbose_name_plural': 'مقادیر پیش فرض مشخصه',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default='وارد نشده', max_length=75, verbose_name='مقدار مشخصه')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='products.product')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productspecifications', verbose_name='مشخصه')),
            ],
            options={
                'verbose_name_plural': 'مشخصات محصول',
                'unique_together': {('specification', 'product')},
            },
        ),
    ]

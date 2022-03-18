from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    exclude = ('slug',)


@admin.register(models.ArticleTag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    readonly_fields = ('date_published', 'author', 'view_count')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)



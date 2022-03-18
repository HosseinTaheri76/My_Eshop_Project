from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from utilties.messaging import get_message
from .models import Category, ProductBrand, ProductSpecifications, Product, ProductSpecificationValue, \
    ProductImageGallery, ProductTag, DefaultSpecificationValue, ProductCollection
from mptt.admin import MPTTModelAdmin
from .forms import ProductSpecificationValueForm


# Register your models here.
class DefaultSpecificationValueInline(admin.TabularInline):
    model = DefaultSpecificationValue
    extra = 1


@admin.register(ProductSpecifications)
class CategorySpecificationAdmin(admin.ModelAdmin):
    inlines = [DefaultSpecificationValueInline]


class CategorySpecificationInline(admin.TabularInline):
    model = ProductSpecifications
    extra = 0
    show_change_link = True


@admin.register(Category)
class ProductCategoryAdmin(MPTTModelAdmin):
    inlines = (CategorySpecificationInline,)
    exclude = ('slug',)


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class ProductGalleryInline(admin.TabularInline):
    model = ProductImageGallery
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecificationValue
    extra = 0
    form = ProductSpecificationValueForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductGalleryInline, ProductSpecificationInline)
    exclude = ('slug', 'user_favorites')
    readonly_fields = ('times_visited', 'date_created', 'date_modified', 'number_sold', 'price')

    def response_post_save_add(self, request, obj):
        messages.add_message(request, messages.INFO, get_message('products/set_specifications'))
        return HttpResponseRedirect(
            reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))

    def get_inlines(self, request, obj):
        if obj:
            return super().get_inlines(request, obj)
        return ProductGalleryInline,


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    fields = ('name', 'categories', 'cover_image')

    def has_add_permission(self, request):
        return self.model.objects.count() < 3

from django.contrib import admin
from .models import SiteInfo, SocialMedia


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 0


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    inlines = [SocialMediaInline]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            SiteInfo.load().save()
        except Exception:
            pass

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

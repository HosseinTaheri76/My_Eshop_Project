from django.contrib import admin
from .models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(is_paid=True)

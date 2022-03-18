from django.contrib import admin

# Register your models here.
from .models import UserMessage


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    fields = ('full_name', 'title', 'phone', 'email', 'question_text', 'date_created', 'is_answered', 'answer_text')
    readonly_fields = ('full_name', 'title', 'phone', 'email', 'question_text', 'date_created')
    list_display = ('full_name', 'title', 'date_created', 'is_answered')
    list_filter = ('is_answered', 'date_created')
    search_fields = ('full_name', 'email', 'title')
    list_editable = ('is_answered',)

    def has_add_permission(self, request):
        return False

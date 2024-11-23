from django.contrib import admin
from .models import Content, UserHistory

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'viewed_at')

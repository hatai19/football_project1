from django.contrib import admin
from .models import Match, Comment

admin.site.register(Match)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'match', 'created',]
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

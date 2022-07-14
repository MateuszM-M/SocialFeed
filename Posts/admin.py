from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_text', 'status', 'slug', 'created_date',
                    'updated_date']
    list_filter = ['created_date']


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'comment_text', 'status', 'created_date',
                    'updated_date']
    list_filter = ['created_date']
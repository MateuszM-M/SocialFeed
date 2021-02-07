from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_text', 'status', 'slug', 'created_date', 'updated_date']
    list_filter = ['created_date']

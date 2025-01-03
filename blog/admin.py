from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'publish']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

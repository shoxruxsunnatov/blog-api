from django.contrib import admin

from posts.models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Post)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
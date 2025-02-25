from django.contrib import admin
from .models import Article, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'location', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'location', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'cover_image')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'location', 'is_published')
        })
    )

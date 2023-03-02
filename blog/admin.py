from django.contrib import admin
from blog.models import Category, Post, Collection, Bookmark, Like
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Category Information'), {'fields': ('title', 'slug')}),
        (_('Content'), {'fields': ('content',)}),
        (_('Post Count'), {'fields': ('show_post_count',)})
    )
    list_display = ('title', 'slug', 'show_post_count')
    search_fields = ('title', 'slug')
    ordering = ('title',)
    readonly_fields = ('show_post_count',)

    # property fieldını da readonly_fields içerisine ekleyerek adminde gösterebiliriz
    def show_post_count(self, obj):
        result = Post.objects.filter(category=obj).count()
        format = format_html("<b>{}</b>", result)
        return format

    show_post_count.short_description = _("Post Count")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Post Information'), {'fields': ('author', 'title', 'subtitle', 'slug', 'image')}),
        (_('Content'), {'fields': ('content',)}),
        (_('Depends'), {'fields': ('category',)}),
        (_('Status'), {'fields': ('status',)}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')})
    )
    list_display = ('title', 'slug', 'author')
    list_filter = ('status',)
    search_fields = ('title', 'slug', 'author__username', 'author__email', 'author__first_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Collection Information'), {'fields': ('user', 'name')}),
        (_('Pin'), {'fields': ('pinned',)}),
    )
    list_display = ('user', 'name')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'name')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Bookmark Information'), {'fields': ('user', 'collection', 'post')}),
        (_('Pin'), {'fields': ('pinned',)}),
    )
    list_display = ('user', 'collection', 'post')
    search_fields = (
        'user__username', 'user__email', 'user__first_name',
        'collection__name', 'post__title', 'post__subtitle', 'post__slug'
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Like Information'), {'fields': ('user', 'post', 'value')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )
    list_display = ('user', 'post', 'value')
    list_filter = ('value',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'post__title', 'post__subtitle', 'post__slug')
    readonly_fields = ('created_at', 'updated_at')

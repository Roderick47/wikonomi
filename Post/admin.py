from django.contrib import admin
from .models import Post, PostLike, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_type_name', 'body_preview', 'like_count', 'comment_count', 'views_count', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('body', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    list_per_page = 50
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Body Preview'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'post__body')
    readonly_fields = ('created_at',)
    list_per_page = 50


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'body_preview', 'is_reply', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('body', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Body Preview'

from django.contrib import admin
from blog.models import Post, Tag, Comment


class AdminPost(admin.ModelAdmin):
    raw_id_fields = ('tags', 'likes', 'author')
    list_display = ('title', 'published_at', 'author')


class AdminComment(admin.ModelAdmin):
    raw_id_fields = ('author', 'post')
    list_display = ('author', 'post', 'text')


admin.site.register(Post, AdminPost)
admin.site.register(Tag)
admin.site.register(Comment, AdminComment)

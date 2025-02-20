from django.contrib import admin
from .models import Forum, Post, Reply, ResourceLink

class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'moderator')

admin.site.register(Forum, ForumAdmin)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(ResourceLink)
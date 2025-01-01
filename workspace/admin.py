from django.contrib import admin
from .models import Workspace, Resource, Chapter, Submission

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('student', 'mentor')
    inlines = [ResourceInline, ChapterInline]

class SubmissionAdmin(admin.ModelAdmin):
   list_display = ('chapter', 'student', 'draft_number', 'status', 'submission_date')
   list_filter = ('status', 'chapter__workspace__student')


admin.site.register(Workspace, WorkspaceAdmin)
admin.site.register(Resource)
admin.site.register(Chapter)
admin.site.register(Submission, SubmissionAdmin)
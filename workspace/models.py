# workspace/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Workspace(models.Model):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workspace'
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='mentored_workspaces',
    )

    def __str__(self):
        return f"{self.student.first_name}'s Workspace"


class Resource(models.Model):
    workspace = models.ForeignKey(
        'Workspace', on_delete=models.CASCADE, related_name='resources'
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='workspace_resources/')

    def __str__(self):
        return self.title


class Chapter(models.Model):
    workspace = models.ForeignKey(
        'Workspace', on_delete=models.CASCADE, related_name='chapters'
    )
    date_added = models.DateTimeField(default=timezone.now)
    chapter_name = models.CharField(max_length=200)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.chapter_name


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('needs_editing', 'Needs Editing'),
    ]

    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    draft_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='workspace_submissions/')
    submission_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    comment = models.TextField(blank=True)
    annotated_file = models.FileField(
        upload_to='workspace_annotations/', blank=True, null=True
    )

    def __str__(self):
        return f"Submission for {self.chapter.chapter_name} (Draft {self.draft_number})"
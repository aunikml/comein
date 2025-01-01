from django.db import models
from django.conf import settings
from django.utils import timezone

class Forum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='forums_created')
    created_at = models.DateTimeField(default=timezone.now)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forums_joined')

    def __str__(self):
        return self.title

class Post(models.Model):
    CONTEXT_CHOICES = [
        ('citation', 'Citation'),
        ('proposal', 'Proposal Writing'),
        ('ai', 'Use of AI'),
        ('plagiarism', 'Plagiarism'),
    ]

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='posts_created')
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    content = models.TextField()
    context = models.CharField(max_length=20, choices=CONTEXT_CHOICES)

    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='replies_created')
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"Reply by {self.created_by.username} on {self.post.title}"

class ResourceLink(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='resource_links')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='resource_links')
    url = models.URLField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.post:
            return f"Resource link for post: {self.post.title}"
        elif self.reply:
            return f"Resource link for reply in post: {self.reply.post.title}"
        else:
            return "Resource link"
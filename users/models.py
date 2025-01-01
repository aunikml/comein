from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager, UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student',
        help_text="Set the user as Student or mentor."
    )

    objects = UserManager()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        default='default_user'  # You can change this default if needed
    )

    password_changed = models.BooleanField(default=False)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    RESEARCH_METHOD_CHOICES = [
        ('quantitative', 'Quantitative'),
        ('qualitative', 'Qualitative'),
        ('mixed', 'Mixed'),
    ]
    preferred_research_methods = models.CharField(
        max_length=20,
        choices=RESEARCH_METHOD_CHOICES,
        blank=True,
        null=True,
    )
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
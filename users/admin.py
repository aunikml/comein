from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from django.utils.translation import gettext_lazy as _
from .forms import UserCreationAdminForm

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
         ('User Type', {'fields': ('user_type',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Password Changed'), {'fields': ('password_changed',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
             'fields': ('username', 'email', 'password', 'first_name', 'last_name','user_type'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active', 'password_changed')
    ordering = ('username',)
    search_fields = ('username', 'first_name', 'last_name')
    add_form = UserCreationAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_type = 'student'  # Set default user type here
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('tinymce/', include('tinymce.urls')),
    path('workspace/', include('workspace.urls')),
    path('forum/', include('forum.urls')),
    path('scheduler/', include('scheduler.urls')),  # Add scheduler URLs
    
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
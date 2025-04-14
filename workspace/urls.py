# workspace/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student/<int:student_id>/', views.workspace_view, name='workspace_view'),
    path('chapter/<int:chapter_id>/edit/', views.edit_chapter, name='edit_chapter'),
    path('chapter/<int:chapter_id>/delete/', views.delete_chapter, name='delete_chapter'),
    path('chapter/<int:chapter_id>/submit/', views.submit_chapter, name='submit_chapter'),
    path('submission/<int:submission_id>/review/', views.review_submission, name='review_submission'),
    path('resource/<int:resource_id>/edit/', views.edit_resource, name='edit_resource'),  # Add this
    path('resource/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),  # Add this
]
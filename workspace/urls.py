from django.urls import path
from .views import workspace_view, submit_chapter, review_submission

urlpatterns = [
    path('student/<int:student_id>/', workspace_view, name='workspace_view'),
    path('chapter/<int:chapter_id>/submit/', submit_chapter, name='submit_chapter'),
    path('submission/<int:submission_id>/review/', review_submission, name='review_submission'),
]

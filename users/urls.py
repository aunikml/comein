from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
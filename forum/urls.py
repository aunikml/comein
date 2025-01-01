from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_forum, name='create_forum'),
]
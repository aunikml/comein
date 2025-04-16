from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('update-calendly/', views.update_calendly_link, name='update_calendly_link'),
]
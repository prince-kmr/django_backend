from django.urls import path
from . import views

urlpatterns = [
    # Leaving the string empty means this is the homepage (e.g., http://127.0.0.1:8000/)
    path('', views.dynamic_home, name='home'),
]
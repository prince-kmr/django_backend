from django.urls import path
from . import views

urlpatterns = [
    # ... your existing url patterns
    path('', views.contact_form_view, name='contact_form'),
    path('articles/', views.article_list, name='article_list'),
    path('page/<slug:slug>/', views.article_detail, name='article_detail'),
]

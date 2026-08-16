from django.urls import path
from .views import RegisterView, LoginView, FirebaseGoogleLoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('firebase-login/', FirebaseGoogleLoginView.as_view(), name='firebase-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

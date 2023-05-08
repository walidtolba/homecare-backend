from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.JSONWebTokenAuth.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('verify-signup/', views.SignupVerificationView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('profile_picture/', views.ProfilePictureView.as_view()),
]

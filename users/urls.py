from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.JSONWebTokenAuth.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('resend_code/', views.ResendVerificationCode.as_view()),
    path('verify-signup/', views.SignupVerificationView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('profile_picture/', views.ProfilePictureView.as_view()),
    path('my_profile/', views.MyProfileView.as_view()),
    path('profile/<int:id>/', views.OtherProfileView.as_view()),
    path('care_about_me/', views.CareAboutMeView.as_view()),
    path('i_care_about/', views.ICareAboutView.as_view()),
    path('profile_picture/<int:id>/', views.ImageAPIView.as_view()),
    path('declare_absance/', views.DeclareAbsance.as_view()),
    path('create_record/', views.CreateVerificationRecordView.as_view()),
    path('reset_password/', views.ResetPassword.as_view()),


]

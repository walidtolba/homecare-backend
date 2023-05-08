from django.urls import path
from . import views

urlpatterns = [
    path('verify_users/', views.verify_users, name='verify_users'),
    path('verify_users/<str:message>', views.verify_users, name='verify_users'),
    path('user_verification_record/<int:pk>', views.user_verification_record_view, name='user_verification_record'),
    path('verification_record/<int:pk>', views.verification_record_view, name='verification_record'),
    path('verify_user_confirm/<int:pk>', views.verify_user_confirm, name='verify_users_confirm'),
    path('verify_user_delete/<int:pk>', views.verify_user_delete, name='verify_users_delete'),
]

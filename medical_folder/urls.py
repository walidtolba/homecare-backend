from django.urls import path
from . import views

urlpatterns = [
    path('my_records/', views.MyRecords.as_view()),
    path('my_reports/', views.MyReports.as_view()),
    path('others_records/<int:id>/', views.OthersRecords.as_view()),
    path('others_reports/<int:id>/', views.OthersReports.as_view()),
    path('others_reports/', views.OthersReportsCreate.as_view()),
]

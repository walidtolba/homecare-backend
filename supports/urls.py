from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.AskSupportView.as_view()),
    path('answer/', views.AnswerSupportView.as_view()),
    path('answer/<int:id>/', views.AnswerSupportView.as_view()),
]
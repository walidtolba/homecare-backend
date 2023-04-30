from django.urls import path
from . import views

urlpatterns = [
    path('my_demands/', views.MyDemandView.as_view()),
    path('tasks/', views.MyTaskView.as_view()),
    path('absances/', views.MyAbsanceView.as_view()),

]

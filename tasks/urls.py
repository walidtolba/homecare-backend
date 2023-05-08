from django.urls import path
from . import views

urlpatterns = [
    path('my_demands/', views.MyDemandView.as_view()),
    path('my_canceled_demands/', views.ListMyCanceledDemandView.as_view()),
    path('my_finished_demands/', views.ListMyFinishedDemandView.as_view()),
    path('tasks/', views.MyTaskView.as_view()),
    path('absances/', views.MyAbsanceView.as_view()),

]

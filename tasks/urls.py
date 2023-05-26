from django.urls import path
from . import views

urlpatterns = [
    path('my_demands/', views.MyDemandView.as_view()),
    path('my_old_demands/', views.MyDemandOldView.as_view()),
    path('others_demands/', views.OtheresDemandView.as_view()),
    path('my_tasks/', views.MyTaskView.as_view()),
    path('my_old_tasks/', views.MyTaskOldView.as_view()),
    path('my_team_members/', views.MyTeamMembersView.as_view()),
    path('my_team_directions/', views.MyTeamDirection.as_view()),
]

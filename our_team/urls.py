from django.urls import path
from our_team.views import create_our_team, delete_our_team, our_teams, update_our_team 

urlpatterns = [
    path('ourteam-list/', our_teams, name = 'ourteam_list'),
    path('create-ourteam/', create_our_team, name = 'create_team'),
    path('update-ourteam/', update_our_team, name = 'update_team'),
    path('delete-ourteam/', delete_our_team, name = 'delete_team'),

]
from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('event/', include('tournament.event_urls')),
    path('tournament/', include('tournament.tournament_urls')),
#urls for team
    path('get-my-team/', views.get_my_team, name='get_my_team'),
    path('create-team-initials/', views.create_team_initials, name='create_team_initials'),
    path('retrieve-team-detail/', views.retrieve_team, name='retrieve_team'),
    path('create-team/', views.create_team, name='create_team'),
    path('update-team/', views.update_team, name='update_team'),
    path('delete-team/', views.delete_team, name='delete_team'),
#urls for eliminationmode
    path('create-elimination-mode/', views.create_elimination_mode, name='create_elimination_mode'),
    path('get-elimination-mode/', views.get_elimination_mode, name='get_elimination_mode'),
    path('get-elimination-mode-list/', views.get_elimination_mode_list, name='elimination_mode_list'),
    path('update-elimination-mode/', views.update_elimination_mode, name='update_elimination_mode'),
    path('delete-elimination-mode/', views.delete_elimination_mode, name='delete_elimination_mode'),
#urls for game
    path('create-game/', views.create_game, name='create_game'),
    path('get-game/', views.get_game, name='get_game'),
    path('game-list/', views.game_list, name='game_list'),
    path('update-game/', views.update_game, name='update_game'),
    path('delete-game/', views.delete_game, name='delete_game'),
]

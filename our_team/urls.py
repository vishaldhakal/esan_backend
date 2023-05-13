from django.urls import path

from our_team.views import OurTeams

urlpatterns = [

    path('ourteam_list/', OurTeams, name = 'ourteam_list')
]
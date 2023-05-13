from django.shortcuts import render
from rest_framework.response import Response
from our_team.models import OurTeam
from our_team.serilaizers import OurTeamSerializer

# Create your views here.
def OurTeams(request):
    teams = OurTeam.objects.all()
    serializers = OurTeamSerializer(teams, many=True)
    return Response(serializers.data)
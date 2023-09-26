from rest_framework.response import Response
from our_team.models import OurTeam
from our_team.serializers import OurTeamSerializer
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['GET'])
def our_teams(request):
    teams = OurTeam.objects.all()
    serializers = OurTeamSerializer(teams, many=True)
    return Response({"teams": serializers.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_our_team(request):
    user = request.user
    if user.role == "Admin":

        name = request.POST.get('name')
        post = request.POST.get('post')
        image = request.FILES.get('image')
        facebook_link = request.POST.get('facebook_link'," ")
        instagram_link = request.POST.get('instagram_link'," ")
        twitch_link = request.POST.get('twitch_link'," ")
        twitter_link = request.POST.get('twitter_link'," ")
        discord_link = request.POST.get('discord_link'," ")
        linkedin_link = request.POST.get('linkedin_link'," ")

        team = OurTeam.objects.create(
            name = name,
            post = post,
            image = image,
            facebook_link = facebook_link,
            instagram_link = instagram_link,
            twitch_link = twitch_link,
            twitter_link = twitter_link,
            discord_link = discord_link,
            linkedin_link = linkedin_link
        ) 
        team.save()
        return Response({"success": "Team member Created Successfully"})
    else:
        return Response({"error":"Unauthourized for creating our_team"},status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_our_team(request):
    idd = int(request.GET.get("id"))
    user = request.user
    if user.role == "Admin":
        team = OurTeam.objects.get(id=idd)
        name = request.POST.get('name')
        post = request.POST.get('post')
        image = request.FILES.get('image')
        facebook_link = request.POST.get('facebook_link'," ")
        instagram_link = request.POST.get('instagram_link'," ")
        twitch_link = request.POST.get('twitch_link'," ")
        twitter_link = request.POST.get('twitter_link'," ")
        discord_link = request.POST.get('discord_link'," ")
        linkedin_link = request.POST.get('linkedin_link'," ")

        team.name = name
        team.post = post
        team.image = image
        team.facebook_link = facebook_link
        team.instagram_link = instagram_link
        team.twitch_link = twitch_link
        team.twitter_link = twitter_link
        team.discord_link = discord_link
        team.linkedin_link = linkedin_link

        team.save()
        return Response({"success": "Team member Updated Successfully"})
    else:
        return Response({"error":"Unauthourized for updating our_team"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_our_team(request):
    idd = int(request.GET.get("id"))
    user = request.user
    if user.role == "Admin":
        team = OurTeam.objects.get(id=idd)
        team.delete()
        return Response({"success":"Team member Deleted Successfully"})
    else:
        return Response({"error":"Unauthourized for updating team members"},status=status.HTTP_401_UNAUTHORIZED)


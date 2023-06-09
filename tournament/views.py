import datetime
from .models import EliminationMode,Team,Game
from account.models import UserProfile,Organization
from account.serializers import UserProfileSerializer
from .serializers import EliminationModeSerializer, GameSerializer,GameSmallSerializer,  TeamSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_team_initials(request):
    user = request.user
    organization = Organization.objects.get(user=user)
    players = organization.players.all()
    teams = Team.objects.filter(organization=organization)
    free_players = players.exclude(id__in=teams.values('players'))
    free_players_ser = UserProfileSerializer(free_players,many=True)
    gamess = Game.objects.all()
    gamess_serializer = GameSmallSerializer(gamess,many=True)
    return Response({"free_players":free_players_ser.data,"games":gamess_serializer.data},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    user = request.user
    if user.role == "Organization":
        players = request.POST.getlist("players")
        manager = request.POST.get("manager")
        team_name = request.POST.get("team_name")
        team_image = request.FILES.get("team_image")
        game_id = request.POST.get("game_id")
        team_type = request.POST.get("team_type", "Squad")  # Default value set to "Squad" if not provided

        organization = Organization.objects.get(user=user)
        game = Game.objects.get(id=game_id)
        manager_profile = UserProfile.objects.get(id=manager)

        team = Team.objects.create(
            team_name=team_name,
            team_image=team_image,
            game=game,
            organization=organization,
            manager=manager_profile,
            team_type=team_type
        )

        players_to_add = UserProfile.objects.filter(id__in=players)
        team.players.set(players_to_add)

        return Response({"success": "Team created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Unauthorized for creating a team"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_team(request):
    user = request.user
    team_id = request.GET.get("id")

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if user.role == "Organization":
        players = request.POST.getlist("players")
        manager = request.POST.get("manager",team.manager.id)
        team_name = request.POST.get("team_name",team.team_name)
        team_image = request.FILES.get("team_image",None)
        game_id = request.POST.get("game_id",team.game.id)
        team_type = request.POST.get("team_type", team.team_type)  # Preserve existing value if not provided

        game = Game.objects.get(id=game_id)
        manager_profile = UserProfile.objects.get(id=manager)

        team.players.clear()
        players_to_add = UserProfile.objects.filter(id__in=players)
        team.players.set(players_to_add)

        print(team_image)
        team.team_name = team_name
        if team_image:
            team.team_image = team_image
        team.manager = manager_profile
        team.game = game
        team.team_type = team_type
        team.save()

        return Response({"success": "Team updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to update the team"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_team(request):
    user = request.user
    team_id = request.POST.get("id")

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if user.role != "Organization":
        return Response({"error": "Unauthorized to delete the team"}, status=status.HTTP_401_UNAUTHORIZED)

    team.delete()

    return Response({"success": "Team deleted"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_team(request):
    user = request.user
    organization = Organization.objects.get(user=user)
    myteams = Team.objects.filter(organization=organization)
    gamess = Game.objects.all()
    gamess_serializer = GameSmallSerializer(gamess,many=True)
    myteams_serializer = TeamSerializer(myteams,many=True)
    return Response({"teams":myteams_serializer.data,"games":gamess_serializer.data},status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_team(request):
    id = request.GET.get("id")
    team = Team.objects.get(id=id)
    serializer = TeamSerializer(team)
    return Response({"team_detail":serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team(request):
    user = request.user
    idd = request.GET.get("id")
    team = Team.objects.get(id=idd)

    if user.role == "Organization":
        team.delete()
        return Response({"success": "Team Deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to delete the team"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_elimination_mode(request):
    user = request.user
    if user.role == "Organizer":
        elimination_mode = request.POST.get('elimination_mode')

        mode = EliminationMode.objects.create(
            elimination_mode=elimination_mode
        )
        mode.save()
        return Response({"success": "Elimination mode created successfully"})
    else:
        return Response({"error": "Unauthorized to creating the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    mode = EliminationMode.objects.get(id=mode_id)
    serializer = EliminationModeSerializer(mode)
    return Response(serializer.data)

@api_view(['GET'])
def get_elimination_mode_list(request):
    elimination_mode = EliminationMode.objects.all()
    serializers = EliminationModeSerializer(elimination_mode, many = True)
    return Response({
        "elimination_modes": serializers.data
    })  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    user = request.user
    if user.role == "Organizer":
        elimination_mode = request.POST.get('elimination_mode')

        mode = EliminationMode.objects.get(id=mode_id)
        mode.elimination_mode = elimination_mode
        mode.save()
        return Response({"success": "Elimination mode updated successfully"})
    else:
        return Response({"error": "Unauthorized to updating the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    user = request.user
    if user.role == "Organizer":
        try:
            mode = EliminationMode.objects.get(id=mode_id)
            mode.delete()
            return Response({"success": "Elimination mode deleted successfully"})
        except EliminationMode.DoesNotExist:
            return Response({"error": "Elimination mode not found"})
    else:
        return Response({"error": "Unauthorized to deleting the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_game(request):
    user = request.user
    if user.role == "Organizer":

        game_name = request.POST.get('game_name')
        game_image = request.POST.get('game_image')
        game_type = request.POST.get('game_type', 'Mobile')
        elimination_modes = request.POST.getlist('elimination_modes')

        game = Game.objects.create(
            game_name=game_name,
            game_image=game_image,
            game_type=game_type
        )

        for mode_id in elimination_modes:
            mode = EliminationMode.objects.get(id=mode_id)
            game.elimination_modes.add(mode)

        return Response({"success": "Game created successfully"})
    else:
        return Response({"error": "Unauthorized to create the game"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_game(request):
    elimination_mode_id = request.GET.get("id")
    elimination_mode = EliminationMode.objects.get(id=elimination_mode_id)
    game = Game.objects.filter(elimination_mode__id=elimination_mode)
    serializer = GameSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def game_list(request):
    game = Game.objects.all()
    serializers = GameSerializer(game, many = True)
    return Response({
        "games": serializers.data
    })  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_game(request):
    game_id = request.GET.get('game_id')
    user = request.user
    if user.role == "Organizer":
        game_name = request.POST.get('game_name')
        game_image = request.POST.get('game_image')
        game_type = request.POST.get('game_type', 'Mobile')
        elimination_modes = request.POST.getlist('elimination_modes')

        try:
            game = Game.objects.get(id=game_id)
            game.game_name = game_name
            game.game_image = game_image
            game.game_type = game_type
            game.elimination_modes.clear()
            
            for mode_id in elimination_modes:
                mode = EliminationMode.objects.get(id=mode_id)
                game.elimination_modes.add(mode)

            game.save()
            return Response({"success": "Game updated successfully"})
        except Game.DoesNotExist:
            return Response({"error": "Game not found"})
    else:
        return Response({"error": "Unauthorized to update the game"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_game(request):
    game_id = request.GET.get('game_id')
    user = request.user
    if user.role == "Organizer":
        try:
            game = Game.objects.get(id=game_id)
            game.delete()
            return Response({"success": "Game deleted successfully"})
        except Game.DoesNotExist:
            return Response({"error": "Game not found"})
    else:
        return Response({"error": "Unauthorized to update the game"}, status=status.HTTP_401_UNAUTHORIZED)



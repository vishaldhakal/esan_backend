import datetime
from .models import EliminationMode, Event, EventFAQ, EventNewsFeed, EventSponsor, Stage,Team,Game, TeamTournamentRegistration, Tournament, TournamentFAQ, TournamentSponsor, TournamentStreams
from account.models import Organizer, UserProfile,Organization
from account.serializers import UserProfileSerializer
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import math
from tournament.models import *
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.core.mail import send_mail

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer":
            return Response({"error": "Only organizers can create events"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get("event_thumbnail")
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description', '')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')
        organizer = Organizer.objects.get(user=user)

        event = Event.objects.create(
            organizer=organizer,
            event_name=event_name,
            event_description=event_description,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            event_thumbnail=event_thumbnail,
            event_thumbnail_alt_description=event_thumbnail_alt_description,
            slug=slug
        )
        event.save()
        return Response({"success": "Successfully created Event"})
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event(request):
    try:
        idd = request.POST.get("id")
        event = Event.objects.get(id=idd)
        user = request.user

        # Check if the user is the organizer of the event
        if event.organizer.user != user:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get('event_thumbnail')
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')

        event.event_name = event_name
        event.slug = slug
        if event_thumbnail:
            event.event_thumbnail = event_thumbnail
        event.event_thumbnail_alt_description = event_thumbnail_alt_description
        event.event_description = event_description
        event.event_start_date = event_start_date
        event.event_end_date = event_end_date

        event.save()
        return Response({"success": "Successfully updated Event"})
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_organizer_events(request):
    user= request.user
    orgg = Organizer.objects.get(user=user)
    event = Event.objects.filter(organizer=orgg)
    serializers = EventDashSerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   

@api_view(["GET"])
def event_list(request):
    user= request.user
    orgg = Organizer.objects.get(user=user)
    event = Event.objects.filter(organizer=orgg)
    serializers = EventVerifySerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   

@api_view(['POST'])
def verify_event(request):
    slug = request.GET.get("slug")
    eventt = Event.objects.get(slug=slug)
    eventt.is_verified = True
    eventt.save()
    return Response({"success":"Verified Sucessfully"},status=200)

@api_view(['POST'])
def verify_team(request):
    iddd = request.GET.get("id")
    regs = TeamTournamentRegistration.objects.get(id=iddd)
    regs.registration_status = "Verified"
    regs.save()
    return Response({"success":"Verified Sucessfully"},status=200)

@api_view(['POST'])
def reject_team(request):
    iddd = request.GET.get("id")
    regs = TeamTournamentRegistration.objects.get(id=iddd)
    regs.registration_status = "Rejected"
    regs.save()
    return Response({"success":"Rejected Sucessfully"},status=200)


@api_view(["GET"])
def all_event_list(request):
    if request.GET.get("all"):
        event = Event.objects.filter(is_published=True)
        serializers = EventVerifySerializer(event, many = True)
        return Response({
            "events": serializers.data
        })
    else:
        event = Event.objects.filter(is_published=True,is_verified=True)
        serializers = EventVerifySerializer(event, many = True)
        return Response({
            "events": serializers.data
        })


@api_view(['GET'])
def event_detail(request):
    slug = request.GET.get('slug')
    event = Event.objects.get(slug = slug)
    event_serializer = EventSerializer(event)
    faq = EventFAQ.objects.filter(event = event)
    faq_serializer = EventFAQSerializer(faq, many = True)
    sponsor = EventSponsor.objects.filter(event = event)
    sponsor_serializer = EventSponsorSerializer(sponsor, many = True)
    return Response({
        'event': event_serializer.data,
        'faqs': faq_serializer.data,
        'sponsors': sponsor_serializer.data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_event(request):
    slug = request.GET.get("slug")
    event = Event.objects.get(slug=slug)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})


@api_view(['GET'])
def get_event_faq(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.filter(event=event)
    faq_ser = EventFAQSerializer(faq,many=True)

    return Response({"FAQs": faq_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_sponsor(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsors = EventSponsor.objects.filter(event=event)
    sponsors_ser = EventSponsorSerializer(sponsors,many=True)

    return Response({"sponsors": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_sponsor_detail(request):
    id = request.GET.get("id")
    sponsors = EventSponsor.objects.get(id=id)
    sponsors_ser = EventSponsorSerializer(sponsors)

    return Response({"sponsor_detail": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_faq(request):
    slug = request.POST.get('slug')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.create(
        event=event,
        value=value,
        heading=heading,
        detail=detail
    )
    faq.save()

    return Response({"success": "Event FAQ created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_faq(request):
    faq_id = request.POST.get('id')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        faq = EventFAQ.objects.get(id=faq_id)
    except EventFAQ.DoesNotExist:
        return Response({"error": "Event FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq.heading = heading
    faq.detail = detail
    faq.save()

    return Response({"success": "Event FAQ updated successfully"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_faq(request):
    id = request.GET.get("id")
    event_faq = EventFAQ.objects.get(id=id)
    event_faq.delete()
    return Response({"success": "EventFAQ deleted successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_news_feed(request):
    slug = request.POST.get('slug')
    content = request.POST.get('content')
    user = request.user
    
    event = Event.objects.get(slug=slug)
    organizer = Organizer.objects.get(user=user)

    news_feed = EventNewsFeed.objects.create(
        event=event,
        content=content,
        user=organizer
    )
    news_feed.save()
    return Response({"success": "Event News Feed created successfully"})

@api_view(['GET'])
def get_event_news_feed(request):
    slug = request.GET.get('slug')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feeds = EventNewsFeed.objects.filter(event=event)
    news_feeds_serializer = EventNewsFeedSerializer(news_feeds, many=True)

    return Response({"news_feeds": news_feeds_serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_news_feed(request):
    news_feed_id = request.GET.get('id')
    content = request.POST.get('content')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.content = content
    news_feed.save()

    return Response({"success": "Event News Feed updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_news_feed(request):
    news_feed_id = request.GET.get('id')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.delete()

    return Response({"success": "Event News Feed deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_sponsor(request):
    slug = request.POST.get('slug')
    sponsor_name = request.POST.get('sponsor_name')
    sponsor_link = request.POST.get('sponsor_link')
    sponsorship_category = request.POST.get('sponsorship_category')
    order = int(request.POST.get('order'))
    sponsor_banner = request.FILES.get('sponsor_banner')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor = EventSponsor.objects.create(
        event=event,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_banner=sponsor_banner,
        sponsor_link=sponsor_link,
        order=order,
    )
    sponsor.save()

    return Response({"success": "Event Sponsor created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_sponsor(request):
    sponsor_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_link = request.POST.get('sponsor_link')
    sponsor_banner = request.FILES.get('sponsor_banner')
    order = int(request.POST.get('order'))

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.sponsor_name = sponsor_name
    sponsor.sponsor_link = sponsor_link
    sponsor.sponsorship_category = sponsorship_category
    sponsor.order = order

    if sponsor_banner:
        sponsor.sponsor_banner = sponsor_banner

    sponsor.save()

    return Response({"success": "Event Sponsor updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_sponsor(request):
    sponsor_id = request.GET.get('id')

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.delete()

    return Response({"success": "Event Sponsor deleted successfully"})



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


@api_view(['GET'])
def tournaments_list(request):
    if request.GET.get("all"):
        tournaments = Tournament.objects.filter(is_published=True)
    else:
        tournaments = Tournament.objects.filter(is_published=True, is_verified=True)
    
    serializers = TournamentSmallestSerializer(tournaments, many=True)
    return Response({
        "tournaments": serializers.data
    })

@api_view(['POST'])
def verify_tournament(request):
    slug = request.GET.get("slug")
    tourn = Tournament.objects.get(slug=slug)
    tourn.is_verified = True
    tourn.save()
    return Response({"success":"Verified Sucessfully"},status=200)


@api_view(['GET'])
def open_tournaments(request):
    current_datetime = datetime.now()
    tournaments = Tournament.objects.filter(is_published=True, registration_opening_date__lte=current_datetime,is_verified=True)
    serializers = TournamentSerializer(tournaments, many=True)
    return Response({
        "tournaments": serializers.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_tournaments_list(request):
    user = request.user
    eslug = request.GET.get("slug")
    event = Event.objects.get(slug=eslug)
    orgg = Organizer.objects.get(user=user)
    tournaments = Tournament.objects.filter(organizer=orgg,event=event)
    serializers = TournamentSerializer(tournaments, many = True)

    return Response({
        "tournaments": serializers.data
    },status=status.HTTP_200_OK)

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer":
            return Response({"error": "Only organizers can create tournaments"}, status=status.HTTP_403_FORBIDDEN)
        slug = request.POST.get('slug')
        tournament_name = request.POST.get('tournament_name', '')
        tournament_slug = request.POST.get('tournament_slug', '')
        tournament_logo = request.FILES.get('tournament_logo', None)
        tournament_banner = request.FILES.get('tournament_banner', None)
        tournament_mode = request.POST.get('tournament_mode', 'Online')
        tournament_start_date = request.POST.get('tournament_start_date', 'Online')
        tournament_end_date = request.POST.get('tournament_end_date', 'Online')
        game_id = request.POST.get('game_id')
        tournament_description = request.POST.get('tournament_description', '')
        tournament_short_description = request.POST.get('tournament_short_description', '')
        
        event = Event.objects.get(slug=slug)
        game = Game.objects.get(id=game_id)
        organizer = Organizer.objects.get(user=user)

        tournament = Tournament(
            organizer=organizer,
            event = event,
            slug=tournament_slug,
            tournament_name=tournament_name,
            tournament_logo=tournament_logo,
            tournament_banner=tournament_banner,
            tournament_mode=tournament_mode,
            game=game,
            tournament_end_date=tournament_end_date,
            tournament_start_date=tournament_start_date,
            tournament_description=tournament_description,
            tournament_short_description=tournament_short_description,
        )
        tournament.save()
        return Response({"success": "Tournament created successfully"})
    except Game.DoesNotExist:
        return Response({"error": "Invalid game ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def tournament_detail(request, slug):
    try:
        matches = []
        tournament = Tournament.objects.get(slug = slug)
        tournament_serializer = TournamentSerializer(tournament)
        stage  = Stage.objects.filter(tournament = tournament)
        stageSerializer = StageSerializer(stage, many = True)
        for s in stageSerializer.data:
            if s['stage_elimation_mode']['id'] == 1:
                round = SingleEliminationRound.objects.filter(stage = s['id'])
                for r in round:
                    match = SingleEliminationMatches.objects.filter(round = r)
                    match_serializer = SingleEliminationMatchSerializer(match, many = True)
                    for ms in match_serializer.data:
                        matches.append(ms)
            else:
                round = DoubleEliminationRound.objects.filter(stage = s['id'])
                for r in round:
                    match = DoubleEliminationMatches.objects.filter(round = r)
                    match_serializer = DoubleEliminationMatchSerializer(match, many = True)
                    for ms in match_serializer.data:
                        matches.append(ms)


        if tournament_serializer.data['tournament_participants'] == 'Team':
            registrations = TeamTournamentRegistration.objects.filter(tournament=tournament)
            serializer = TeamTournamentRegistrationSerializer(registrations, many=True)
        else:
            registrations = SoloTournamentRegistration.objects.filter(tournament=tournament)
            serializer = SoloTournamentRegistrationSerializer(registrations, many=True)
        prize_pool = TournamentPrizePool.objects.filter(tournament=tournament)
        prize_serializer = TournamentPrizePoolSerializer(prize_pool,many=True)

        return Response({
            'status':200,
            'tournament': tournament_serializer.data,
            'teams': serializer.data,
            'prizes': prize_serializer.data,
            'matches': matches
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def tournament_details(request):
    slug = request.GET.get("slug") 
    tournament = Tournament.objects.get(slug = slug)
    tournament_serializer = TournamentSerializer(tournament)
    if tournament_serializer.data['tournament_participants'] == 'Team':
            registrations = TeamTournamentRegistration.objects.filter(tournament=tournament)
            serializer = TeamTournamentRegistrationSerializer(registrations, many=True)
    else:
        registrations = SoloTournamentRegistration.objects.filter(tournament=tournament)
        serializer = SoloTournamentRegistrationSerializer(registrations, many=True)
    return Response({
        'tournament': tournament_serializer.data,
        'teams': serializer.data,

    })
   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament(request):
    slug = request.POST.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    user = request.user

    # Check if the current user is authorized to update the tournament
    if tournament.organizer.user != user:
        return Response({"error": "You are not authorized to update this Tournament"}, status=status.HTTP_403_FORBIDDEN)

    tournament.tournament_name = request.POST.get('tournament_name', tournament.tournament_name)
    tournament_logo = request.FILES.get('tournament_logo')
    if tournament_logo:
        tournament.tournament_logo = tournament_logo
    tournament_banner = request.FILES.get('tournament_banner')
    if tournament_banner:
        tournament.tournament_banner = tournament_banner
    tournament.location = request.POST.get('location', tournament.location)
    tournament.tournament_mode = request.POST.get('tournament_mode', tournament.tournament_mode)
    tournament.is_free = bool(request.POST.get('is_free', tournament.is_free)=='True')
    tournament.tournament_fee = request.POST.get('tournament_fee', tournament.tournament_fee)
    tournament.maximum_no_of_participants = request.POST.get('maximum_no_of_participants', tournament.maximum_no_of_participants)
    tournament.tournament_description = request.POST.get('tournament_description', tournament.tournament_description)
    tournament.tournament_short_description = request.POST.get('tournament_short_description', tournament.tournament_short_description)
    tournament.tournament_rules = request.POST.get('tournament_rules', tournament.tournament_rules)
    tournament.tournament_prize_pool = request.POST.get('tournament_prize_pool', tournament.tournament_prize_pool)
    tournament.registration_opening_date = request.POST.get('registration_opening_date', tournament.registration_opening_date)
    tournament.registration_closing_date = request.POST.get('registration_closing_date', tournament.registration_closing_date)
    tournament.tournament_start_date = request.POST.get('tournament_start_date', tournament.tournament_start_date)
    tournament.tournament_end_date = request.POST.get('tournament_end_date', tournament.tournament_end_date)
    tournament.is_published = bool(request.POST.get('is_published', tournament.is_published))
    tournament.is_registration_enabled = bool(request.POST.get('is_registration_enabled', tournament.is_registration_enabled))
    tournament.accept_registration_automatic = bool(request.POST.get('accept_registration_automatic', tournament.accept_registration_automatic))
    tournament.contact_email = request.POST.get('contact_email', tournament.contact_email)
    tournament.discord_link = request.POST.get('discord_link', tournament.discord_link)
    tournament.live_link = request.POST.get('live_link', tournament.live_link)
    tournament.save()
    return Response({"success": "Tournament updated successfully"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    tournament.delete()
    return Response({"success": "Tournament deleted successfully"})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_sponsor(request):
    slug = request.POST.get('slug')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_link = request.POST.get('sponsor_link')
    sponsor_banner = request.FILES.get('sponsor_banner')
    order = int(request.POST.get('order'))

    try:
        tournament = Tournament.objects.get(slug=slug)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_sponsor = TournamentSponsor.objects.create(
        tournament=tournament,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_banner=sponsor_banner,
        order=order,
        sponsor_link=sponsor_link,
    )
    tournament_sponsor.save()
    return Response({"success": "TournamentSponsor created successfully"})

@api_view(['GET'])
def get_tournament_sponsor_list(request):
    tournament_sponsors = TournamentSponsor.objects.all()
    serializer = TournamentSponsorSerializer(tournament_sponsors, many=True)
    return Response({"tournament_sponsors": serializer.data})


@api_view(['GET'])
def get_tournament_sponsor(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    sponsor = TournamentSponsor.objects.filter(tournament = tournament)
    serializer = TournamentSponsorSerializer(sponsor,many=True)
    return Response({"sponsors":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament_sponsor(request):
    sponsor_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_link = request.POST.get('sponsor_link')
    sponsor_banner = request.FILES.get('sponsor_banner',None)
    order = int(request.POST.get('order'))

    try:
        tournament_sponsor = TournamentSponsor.objects.get(id=sponsor_id)
    except TournamentSponsor.DoesNotExist:
        return Response({"error": "Tournament Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_sponsor.sponsor_name = sponsor_name
    tournament_sponsor.sponsor_link = sponsor_link
    tournament_sponsor.order = order
    tournament_sponsor.sponsorship_category = sponsorship_category
    if sponsor_banner:
        tournament_sponsor.sponsor_banner = sponsor_banner

    tournament_sponsor.save()
    return Response({"success": "TournamentSponsor updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_sponsor(request):
    sponsor_id = request.GET.get("id")
    tournament_sponsor = TournamentSponsor.objects.get(id=sponsor_id)
    tournament_sponsor.delete()
    return Response({"success": "TournamentSponsor deleted successfully"})

# prize 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_prize_pool(request):
    slug = request.POST.get('slug')
    placement = request.POST.get('placement')
    prize = request.POST.get('prize')
    try:
        tournament = Tournament.objects.get(slug=slug)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_prize = TournamentPrizePool.objects.create(
        tournament=tournament,
        placement=placement,
        prize=prize,
    )
    tournament_prize.save()
    return Response({"success": "TournamentPrize created successfully"})

@api_view(['GET'])
def get_tournament_prizes_list(request):
    tournament_prizes = TournamentPrizePool.objects.all()
    serializer = TournamentPrizePoolSerializer(tournament_prizes, many=True)
    return Response({"tournament_prizes": serializer.data})


@api_view(['GET'])
def get_tournament_prizes(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    prizes = TournamentPrizePool.objects.filter(tournament = tournament)
    serializer = TournamentPrizePoolSerializer(prizes,many=True)
    return Response({"Prizes":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament_prize(request):
    prize_pool_id = request.POST.get('id')
    placement = request.POST.get('placement')
    prize = request.POST.get('prize')

    print(prize_pool_id)
    try:
        tournament_prize = TournamentPrizePool.objects.get(id=prize_pool_id)
    except TournamentSponsor.DoesNotExist:
        return Response({"error": "Tournament Prize does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_prize.placement = placement
    tournament_prize.prize = prize
    tournament_prize.save()
    return Response({"success": "TournamentPrize updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_prize(request):
    prize_pool_id = request.GET.get("id")
    tournament_prize = TournamentPrizePool.objects.get(id=prize_pool_id)
    tournament_prize.delete()
    return Response({"success": "TournamentPrize deleted successfully"})
   
# prize end
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_faq(request):
    slug = request.POST.get('slug')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        tournament = Tournament.objects.get(slug=slug)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_faq = TournamentFAQ.objects.create(
        tournament = tournament,
        value=value,
        heading=heading,
        detail=detail
    )
    tournament_faq.save()
    return Response({"success": "TournamentFAQ created successfully"})


@api_view(['GET'])
def get_tournament_faq_list(request):
    tournament_faqs = TournamentFAQ.objects.all()
    serializer = TournamentFAQSerializer(tournament_faqs, many=True)
    return Response({"tournament_faqs": serializer.data})


@api_view(['GET'])
def get_tournament_faq(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    faq = TournamentFAQ.objects.filter(tournament = tournament)
    serializer = TournamentFAQSerializer(faq,many=True)
    return Response({"FAQs":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament_faq(request):
    faq_id = request.POST.get('id')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        tournament_faq = TournamentFAQ.objects.get(id=faq_id)
    except TournamentFAQ.DoesNotExist:
        return Response({"error": "Tournament FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_faq.heading = heading
    tournament_faq.detail = detail

    tournament_faq.save()
    return Response({"success": "TournamentFAQ updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_faq(request):
    faq_id = request.GET.get("id")
    tournament_faq = TournamentFAQ.objects.get(id=faq_id)
    tournament_faq.delete()
    return Response({"success": "TournamentFAQ deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_stream(request):
    user = request.user
    if user.role == "Organizer":
        slug = request.POST.get('slug')
        stream_title = request.POST.get('stream_title')
        url = request.POST.get('url')

        try:
            tournament = Tournament.objects.get(slug=slug)
        except Tournament.DoesNotExist:
            return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)
        tournament_stream = TournamentStreams.objects.create(
            tournament = tournament,
            stream_title = stream_title,
            url = url
        )
        tournament_stream.save()
        return Response({"success": "Tournament Stream created successfully"})
    else:
        return Response({"error": "Unauthorized to create the Tournament Stream"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_tournament_stream(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    tournament_stream= TournamentStreams.objects.filter(tournament=tournament)
    serializer = TournamentStreamsSerializer(tournament_stream, many=True)
    return Response({"tournament_streams": serializer.data})


@api_view(['GET'])
def get_tournament_stream_list(request):
    pk = request.GET.get('id')
    stream = TournamentStreams.objects.get(id = pk)
    serializer = TournamentStreamsSerializer(stream)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament_stream(request):
    stream_id = request.POST.get('id')
    user = request.user

    if user.role == "Organizer":
        stream_title = request.POST.get('stream_title')
        url = request.POST.get('url')

        try:
            stream = TournamentStreams.objects.get(id=stream_id)
        except TournamentStreams.DoesNotExist:
            return Response({"error": "Tournament stream not found"})
        stream.stream_title = stream_title
        stream.url = url
        stream.save()

        return Response({"success": "Tournament stream updated successfully"})
        
    else:
        return Response({"error": "Unauthorized to update the tournament stream"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_stream(request):
    stream_id = request.GET.get("id")
    user = request.user

    if user.role == "Organizer":
        tournament_stream = TournamentStreams.objects.get(id=stream_id)
        tournament_stream.delete()
        return Response({"success": "TournamentStream deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the tournament stream"}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(["GET"])
def get_stage(request):
    slug = request.GET.get("slug")
    tournament = Tournament.objects.get(slug=slug)
    stages = Stage.objects.filter(tournament=tournament)
    serializer = StageSerializer(stages, many=True)
    return Response({"stages": serializer.data})


@api_view(['GET'])
def get_stage_list(request):
    pk = request.GET.get('id')
    try:
        stage = Stage.objects.get(id=pk)
        serializer = StageSerializer(stage)
        return Response(serializer.data)
    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stage(request):
    try:
        tournament_slug = request.POST.get("tournament_slug")
        print(tournament_slug)
        tournament = Tournament.objects.get(slug=tournament_slug)
        stage_number = request.POST.get('stage_number')
        stage_name = request.POST.get('stage_name')
        stage_elimation_mode_id = int(request.POST.get('stage_elimation_mode'))
        input_no_of_teams = request.POST.get('input_no_of_teams')
        output_no_of_teams = request.POST.get('output_no_of_teams')

        elimination_mode = EliminationMode.objects.get(id=stage_elimation_mode_id)
        
        stage = Stage.objects.create(
            stage_number=stage_number,
            stage_name=stage_name,
            stage_elimation_mode=elimination_mode,
            input_no_of_teams=input_no_of_teams,
            output_no_of_teams=output_no_of_teams,
            tournament=tournament
        )
        stage.save()
        if stage_elimation_mode_id == 1:
            total_matches_rounds = calculate_rounds_matches(int(input_no_of_teams))
            find_stage = Stage.objects.get(id = stage.id)
            for index, matches in enumerate(total_matches_rounds[1]):
                SER =  SingleEliminationRound.objects.create(
                    round_name = f"Round {index + 1}",
                    start_date_time = datetime.datetime.now(), 
                    number_of_matches = matches,
                    stage = find_stage
                )

                SER.save()
                find_round = SingleEliminationRound.objects.get(id = SER.id)
                for i in range(matches):
                    SEM = SingleEliminationMatches.objects.create(
                        match_name = f"Match {i+1}",
                        round = find_round,
                        start_date_time = datetime.datetime.now()
                    )

                    SEM.save()
        elif stage_elimation_mode_id == 2:
            total_matches_rounds = generate_double_elimination_matches(int(input_no_of_teams))
            find_stage = Stage.objects.get(id = stage.id)
            WB = total_matches_rounds['WB'][1]
            LB = total_matches_rounds['LB'][1]
            for index, matches in enumerate(WB):
                SER =  DoubleEliminationRound.objects.create(
                    round_name = f"Round {index + 1}",
                    start_date_time = datetime.datetime.now(), 
                    number_of_matches = matches,
                    stage = find_stage,
                    bracket = 'WB',

                )

                SER.save()
                find_round = DoubleEliminationRound.objects.get(id = SER.id)
                for i in range(matches):
                    SEM = DoubleEliminationMatches.objects.create(
                        match_name = f"Match {i+1}",
                        round = find_round,
                        start_date_time = datetime.datetime.now()
                        
                    )

                    SEM.save()
            for index, matches in enumerate(LB):
                SER =  DoubleEliminationRound.objects.create(
                    round_name = f"Round {index + 1}",
                    start_date_time = datetime.datetime.now(), 
                    number_of_matches = matches,
                    stage = find_stage,
                    bracket = 'LB',

                )

                SER.save()
                find_round = DoubleEliminationRound.objects.get(id = SER.id)
                for i in range(matches):
                    SEM = DoubleEliminationMatches.objects.create(
                        match_name = f"Match {i+1}",
                        round = find_round,
                        start_date_time = datetime.datetime.now()
                        
                    )

                    SEM.save()

        elif stage_elimation_mode_id == 3:
            find_stage = Stage.objects.get(id = stage.id)
            bRM = BattleRoyalMatch.objects.create(
                stage = find_stage
            )
            bRM.save()

        return Response({"success": "Stage created successfully"})
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament not found"}, status=status.HTTP_400_BAD_REQUEST)
    except EliminationMode.DoesNotExist:
        return Response({"error": "Invalid elimination mode ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Team.DoesNotExist:
        return Response({"error": "Invalid team ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_stage(request):
    try:
        stage_id = request.GET.get("id")
        stage = Stage.objects.get(id=stage_id)

        stage_number = request.POST.get('stage_number', stage.stage_number)
        stage_name = request.POST.get('stage_name', stage.stage_name)
        stage_elimation_mode_id = request.POST.get('stage_elimation_mode_id', stage.stage_elimation_mode_id)
        input_no_of_teams = request.POST.get('input_no_of_teams', stage.input_no_of_teams)
        output_no_of_teams = request.POST.get('output_no_of_teams', stage.output_no_of_teams)
        input_team_ids = request.POST.getlist('input_team_ids', list(stage.input_teams.values_list('id', flat=True)))
        output_team_ids = request.POST.getlist('output_team_ids', list(stage.output_teams.values_list('id', flat=True)))

        if stage_elimation_mode_id:
            elimination_mode = EliminationMode.objects.get(id=stage_elimation_mode_id)
            stage.stage_elimation_mode = elimination_mode

        stage.stage_number = stage_number
        stage.stage_name = stage_name
        stage.input_no_of_teams = input_no_of_teams
        stage.output_no_of_teams = output_no_of_teams
        stage.save()

        input_teams = Team.objects.filter(id__in=input_team_ids)
        stage.input_teams.set(input_teams)

        output_teams = Team.objects.filter(id__in=output_team_ids)
        stage.output_teams.set(output_teams)

        return Response({"success": "Stage updated successfully"})
    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
    except EliminationMode.DoesNotExist:
        return Response({"error": "Invalid elimination mode ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Team.DoesNotExist:
        return Response({"error": "Invalid team ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stage(request):
    try:
        stage_id = request.data['id']
        stage = Stage.objects.get(id=stage_id)
        stage.delete()
        return Response({"success": "Stage deleted successfully"})
    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def registered_teams(request):
    slug = request.GET.get("slug")
    
    user = request.user

    if user.role == "Organizer":
        tournament = Tournament.objects.get(slug=slug)
        registrations = TeamTournamentRegistration.objects.filter(tournament=tournament)
        serializer = TeamTournamentRegistrationSerializer(registrations, many=True)
        return Response({"registrations": serializer.data})
    else:
        return Response({"error": "Unauthorized to view registered teams"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def open_tournament_registration(request):
    slug = request.POST.get('slug')
    registration_opening_date = request.POST.get('registration_opening_date')
    registration_closing_date = request.POST.get('registration_closing_date')

    try:
        tournament = Tournament.objects.get(slug=slug)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    is_free = request.POST.get('is_free',False)=="True"
    tournament.is_free = is_free

    if is_free: 
        tournament.tournament_fee = 0
    else:
        fee = request.POST.get('tournament_fee') 
        tournament.tournament_fee = float(fee)

    tournament.registration_opening_date = registration_opening_date
    tournament.registration_closing_date = registration_closing_date
    tournament.is_published = True
    tournament.is_registration_enabled = True
    tournament.accept_registration_automatic = True

    tournament_rules = request.POST.get('tournament_rules')
    tournament.tournament_rules = tournament_rules

    tournament_prize_pool = request.POST.get('tournament_prize_pool')
    tournament.tournament_prize_pool = tournament_prize_pool
    
    maximum_no_of_participants = request.POST.get('maximum_no_of_participants')
    tournament.maximum_no_of_participants = maximum_no_of_participants

    contact_email = request.POST.get('contact_email'," ")
    tournament.contact_email = contact_email

    discord_link = request.POST.get('discord_link'," ")
    tournament.discord_link = discord_link

    location = request.POST.get('location'," ")
    tournament.location = location

    tournament.tournament_status = "Live"

    tournament_participants = request.POST.get('tournament_participants')
    tournament.tournament_participants = tournament_participants
    tournament.save()

    return Response({"success": "Registration opened for the tournament"})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def register_team_initials(request):
    
    slug = request.GET.get('slug')
    try:
        user = request.user
        orgg = Organization.objects.get(user=user)
    except Organization.DoesNotExist or Exception:
        return Response({"error": "No organization found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        tournament = Tournament.objects.get(slug=slug)
    except (Tournament.DoesNotExist, Team.DoesNotExist):
        return Response({"error": "Invalid tournament or team"}, status=404)

    gam = tournament.game
    registeredteams = TeamTournamentRegistration.objects.filter(tournament=tournament,team__organization=orgg)
    ts = TeamTournamentRegistrationSerializer(registeredteams,many=True)
    teamss = Team.objects.filter(organization=orgg,game=gam)
    teamss_ser = TeamRegisterSerializer(teamss,many=True)

    soloRegisterTeamsList = []
    soloRegisteredTeams = SoloTournamentRegistration.objects.filter(tournament=tournament)
    soloRegisteredTeamsSerializer = SoloTournamentRegistrationSerializer(soloRegisteredTeams, many = True)

    players = []
    organizationSerializer = OrganizationSerializer(orgg, many = False)
    for p in organizationSerializer.data['players']:
        user = UserProfile.objects.get(id = p)
        userSerializer = UserProfileSerializer(user, many = False)
        players.append(userSerializer.data)
        
        for pl in soloRegisteredTeamsSerializer.data:
            user = UserProfile.objects.get(id = pl['player'])
            userSoloSerializer = UserProfileSerializer(user, many = False)
            if userSoloSerializer.data['id'] == userSerializer.data['id']:
                if len(soloRegisterTeamsList) > 0:
                    for so in soloRegisterTeamsList:
                        if not so['id'] == userSoloSerializer.data['id']:
                            soloRegisterTeamsList.append(userSoloSerializer.data)
                else:
                    soloRegisterTeamsList.append(userSoloSerializer.data)

    return Response({"teams": teamss_ser.data,"registered_teams":ts.data, 'players': players, 'soloRegisteredPlayers':soloRegisterTeamsList})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_team(request):
    user = request.user
    slug = request.POST.get('slug')
    team_id = request.POST.get('team_id')
    registration_status = request.POST.get('registration_status', 'Ongoing Review')
    payment_method = request.POST.get('payment_method', 'Other')

    try:
        tournament = Tournament.objects.get(slug=slug)
        team = Team.objects.get(id=team_id)
        tss = TeamTournamentRegistration.objects.filter(team=team, tournament = tournament)
        if tss:
            return Response({"error": f"This team is already registered on ${tournament.tournament_name}"}, status=status.HTTP_406_NOT_ACCEPTABLE)    
    except (Tournament.DoesNotExist, Team.DoesNotExist):
        return Response({"error": "Invalid tournament or team"}, status=404)

    if user.role == "Organization" or "Admin":
            registration = TeamTournamentRegistration.objects.create(
                tournament=tournament,
                team=team,
                registration_status=registration_status,
                payment_method=payment_method,
            )
            registration.save()
            return Response({"success": "Team registered successfully"})
    else:
        return Response({"error": "Unauthorized to register a team"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_solo_player(request):
    slug = request.POST.get('slug')
    registration_status = request.POST.get('registration_status', 'Ongoing Review')
    registration_date = request.POST.get('registration_date')
    registration_fee = request.POST.get('registration_fee')
    payment_method = request.POST.get('payment_method', 'Other')
    try:
        tournament = Tournament.objects.get(slug=slug)
        player = UserProfile.objects.get(id=request.POST.get('player'))
        pss = SoloTournamentRegistration.objects.filter(player=player, tournament = tournament).exists()
        if pss:
            return Response({"error": f"This player is already registered on {tournament.tournament_name}"}, status=status.HTTP_406_NOT_ACCEPTABLE)    
    
        registration = SoloTournamentRegistration.objects.create(
                tournament=tournament,
                player=player,
                registration_status=registration_status,
                registration_date = registration_date,
                registration_fee = registration_fee,
                payment_method=payment_method,
            )
        registration.save()
        return Response({"success": "You are successfully registered as a player"})
    
    except (Tournament.DoesNotExist, UserProfile.DoesNotExist):
        return Response({"error": "Invalid tournament or player"}, status=404)
    
@api_view(['GET'])
def get_solo_registered_players_tournament(request, slug):
    try:
        players = []
        tournament = Tournament.objects.get(slug = slug)
        register_solo_player = SoloTournamentRegistration.objects.filter(tournament = tournament)
        rspSerializer = SoloTournamentRegistrationSerializer(register_solo_player, many = True)
        for plr in rspSerializer.data:
            player = UserProfile.objects.get(id = plr['player'])
            playerSerializer = UserProfileSerializer(player, many = False)
            players.append(playerSerializer.data)
        return Response({'status':200, "players":players})
    except Exception as e:
        return Response({'status':500, "message": str(e)})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_the_team_player_status(request):
    try:
        data = request.data
        id = data['team_or_player_id']
        teamOrPlayerType = data['team_player_type']
        registration_status = data['registration_status']
        slug = data['slug']
        tournament = Tournament.objects.get(slug = slug)
        if teamOrPlayerType == "Team":
            team = Team.objects.get(id = id)
            teamRegistered = TeamTournamentRegistration.objects.get(tournament = tournament, team = team)
            teamRegistered.registration_status = registration_status
            teamRegistered.save()
            if registration_status == "Rejected":
                send_mail(
                    'ESSAN Rejection Message',
                    f"Hello {request.user.username},{request.data['message']}",
                    'manishregmi39@gmail.com',
                    [request.user.email],
                    fail_silently=False,
                    )
            return Response({'status':200, "message":f"Status of {team.team_name} changed to {registration_status} successfully"})
        
        elif teamOrPlayerType == "Player":
            player = UserProfile.objects.get(id = id)
            soloRegistered = SoloTournamentRegistration.objects.get(tournament = tournament, player = player)
            soloRegistered.registration_status = registration_status
            soloRegistered.save()
            if registration_status == "Rejected":
                send_mail(
                    'ESSAN Rejection Message',
                    f"Hello {player.name},{request.data['message']}",
                    'manishregmi39@gmail.com',
                    [player.email],
                    fail_silently=False,
                    )
            return Response({'status':200, "message":f"Status of {player.username} changed to {registration_status} successfully"})

    except Tournament.DoesNotExist:
        return Response({'status':404, "message":"Tournament doesnot exists"})
    
    except TeamTournamentRegistration.DoesNotExist:
        return Response({'status':404, "message":"This team is not registered in any tournament"})
    
    except SoloTournamentRegistration.DoesNotExist:
        return Response({'status':404, "message":"This player is not registered in any tournament"})
    
    except Exception as e:
        return Response({'status':500, "message":str(e)})

@api_view(['GET'])
def get_players_acc_to_organization(request, id):
    try:
       players = []
       organization = Organization.objects.get(id = id)
       organizationSerializer = OrganizationSerializer(organization, many = False)
       for p in organizationSerializer.data['players']:
           user = UserProfile.objects.get(id = p)
           userSerializer = UserProfileSerializer(user, many = False)
           players.append(userSerializer.data)
       return Response({'status':200, "players":players})
    except Exception as e:
        return Response({'status':500, "message": str(e)})
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_team_registration(request):
    registration_id = request.GET.get('id')
    user = request.user

    if user.role == "Organizer":
        team_id = request.POST.get('team_id')
        registration_fee = request.POST.get('registration_fee')
        registration_status = request.POST.get('registration_status')
        payment_method = request.POST.get('payment_method')
        current_stage_id = request.POST.get('id')

        try:
            team_registration = TeamTournamentRegistration.objects.get(id=registration_id)
            team = Team.objects.get(id=team_id)
            current_stage = Stage.objects.get(id=current_stage_id) 
        except (TeamTournamentRegistration.DoesNotExist, Team.DoesNotExist, Stage.DoesNotExist):
            return Response({"error": "Invalid team registration, team, or current stage"})

        team_registration.team = team
        team_registration.registration_fee = registration_fee
        team_registration.registration_status = registration_status
        team_registration.payment_method = payment_method
        team_registration.current_stage = current_stage

        team_registration.save()
        return Response({"success": "Team registration updated successfully"})
    else:
        return Response({"error": "Unauthorized to update the team registration"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team_registration(request):
    registration_id = request.GET.get("id")
    user = request.user

    if user.role == "Organization":
        try:
            team_registration = TeamTournamentRegistration.objects.get(id=registration_id)
        except TeamTournamentRegistration.DoesNotExist:
            return Response({"error": "Team registration not found"})
        team_registration.delete()
        return Response({"success": "Team registration deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the team registration"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getBracketsOfStage(request):
    try:    
        elemination_type =  request.POST.get('elemination_type')
        stage_id = request.POST.get('stage_id')
        if elemination_type is None or stage_id is None:
            return Response({'message':"Fields cannot be null", "status":500})
        if elemination_type == "2":
            round = DoubleEliminationRound.objects.filter(stage_id = stage_id)
            serializer = DoubleEliminationRoundSerializer(round, many = True)
            for match in serializer.data:
                matches = DoubleEliminationMatches.objects.filter(round_id = match['id'])
                mserializer = DoubleEliminationMatchSerializer(matches, many = True)
                match['matches'] = mserializer.data
            return Response({'brackets':serializer.data, "status": 200})
        
        elif elemination_type == "1":
            round = SingleEliminationRound.objects.filter(stage_id = stage_id)
            serializer = SingleEliminationRoundSerializer(round, many = True)
            for match in serializer.data:
                matches = SingleEliminationMatches.objects.filter(round_id = match['id'])
                mserializer = SingleEliminationMatchSerializer(matches, many = True)
                match['matches'] = mserializer.data
            return Response({'brackets':serializer.data, "status": 200})
    except Exception as e:
        return Response({'status':500, "message": str(e)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateRoundOrMatchesOfSingleElimination(request):
    data = request.data
    type = data['update_type']
    id = data['round_or_match_id']
    try:
        if type == 'Match':
            match = SingleEliminationMatches.objects.get(id = id)
            if not match:
                return Response({'status':400, "message":'No match found'})
            serializer =  SingleEliminationMatchSerializer(match, data=request.POST, many = False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status':200, "message":"Updated successfully"})
            else:
                return Response({'status':400, 'message':"Cannot update match"})
        
        else:
            match = SingleEliminationRound.objects.get(id = id)
            if not match:
                return Response({'status':400, "message":'No Round found'})
            serializer =  SingleEliminationRoundSerializer(match, data=request.POST, many = False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status':200, "message":"Updated successfully"})
            else:
                return Response({'status':400, 'message':"Cannot update match"})
            
    except Exception as e:
        print(e)
        return Response(str(e))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateRoundOrMatchesOfDoubleElimination(request):
    data = request.data
    type = data['update_type']
    id = data['round_or_match_id']
    try:
        if type == 'Match':
            match = DoubleEliminationMatches.objects.get(id = id)
            if not match:
                return Response({'status':400, "message":'No match found'})
            serializer =  DoubleEliminationMatchSerializer(match, data=request.POST, many = False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status':200, "message":"Updated successfully"})
            else:
                return Response({'status':400, 'message':"Cannot update match"})
        
        else:
            match = DoubleEliminationRound.objects.get(id = id)
            if not match:
                return Response({'status':400, "message":'No Round found'})
            serializer =  DoubleEliminationRoundSerializer(match, data=request.POST, many = False)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status':200, "message":"Updated successfully"})
            else:
                return Response({'status':400, 'message':"Cannot update match"})
            
    except Exception as e:
        return Response(str(e))

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def getMatchesOfStages(request):
    try:    
        stage_id = request.POST.get('stage_id')
        mode_type = int(request.POST.get('mode_id'))
        matchList = []
        if mode_type == 1:
            round = SingleEliminationRound.objects.filter(stage = stage_id)
            for r in round:
                getRound = SingleEliminationRound.objects.get(id = r.id)
                sGetRound = SingleEliminationRoundSerializer(getRound, many = False)
                matches = SingleEliminationMatches.objects.filter(round = r).order_by('-id')
                serializer = SingleEliminationMatchSerializer(matches, many = True)
                for s in serializer.data:
                    s['round'] = sGetRound.data
                    matchList.append(s)
            return Response({'status':200, "matches": matchList})
        
        if mode_type == 2:
            round = DoubleEliminationRound.objects.filter(stage = stage_id)
            for r in round:
                getRound = DoubleEliminationRound.objects.get(id = r.id)
                sGetRound = DoubleEliminationRoundSerializer(getRound, many = False)
                matches = DoubleEliminationMatches.objects.filter(round = r).order_by('-id')
                serializer = DoubleEliminationMatchSerializer(matches, many = True)
                for s in serializer.data:
                    s['round'] = sGetRound.data
                    matchList.append(s)
            return Response({'status':200, "matches": matchList})
        
    except DoubleEliminationRound.DoesNotExist:
        return Response({'status':404, 'message': "Round doesnot exists"})
    
    except SingleEliminationMatches.DoesNotExist:
        return Response({'status':404, 'message': "Match doesnot exists"})
    
    except DoubleEliminationRound.DoesNotExist:
        return Response({'status':404, 'message': "Round doesnot exists"})
    
    except DoubleEliminationMatches.DoesNotExist:
        return Response({'status':404, 'message': "Match doesnot exists"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_battle_royal_match_details(request):
    try:
        match_details_id = request.data['match_details_id']
        update_type = request.data['update_type']
        if update_type == "Team":
            match = BattleRoyalTeamDetails.objects.get(id = match_details_id)
            match_update = BattleRoyalTeamDetailsSerializer(match, data=request.data, many = False)
            if match_update.is_valid(raise_exception=True):
                match_update.save()
                return Response({'status':200, "message":"Teams details updated successfully"})
        else:
            match = BattleRoyalPlayerDetails.objects.get(id = match_details_id)
            match_update = BattleRoyalPlayerDetailsSerializer(match, data=request.data, many = False)
            if match_update.is_valid(raise_exception=True):
                match_update.save()
                return Response({'status':200, "message":"Players details updated successfully"})

    except Exception as e:
        return Response({"status":500, "message":str(e)})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_battle_royale_match_details(request):
    try:
        stage_id = request.data['stage_id']
        create_type = request.data['create_type']
        stage = Stage.objects.get(id = stage_id)
        battleRoyale = BattleRoyalMatch.objects.get(stage = stage)
        if create_type == "Team":
            for team in request.data['teams']:
                myTeam = Team.objects.get(id = team)
                bRMPD = BattleRoyalTeamDetails.objects.create(
                    battleRoyale = battleRoyale,
                    team = myTeam,
                )
                bRMPD.save()
            return Response({'status':200, "message":"Details for teams created successfully"})
        else:
            for player in request.data['players']:
                myPlayer = UserProfile.objects.get(id = player)
                bRMPD = BattleRoyalPlayerDetails.objects.create(
                    battleRoyale = battleRoyale,
                    players = myPlayer,
                )
                bRMPD.save()
            return Response({'status':200, "message":"Details for players created successfully"})

    except Exception as e:
        return Response({"status":500, "message":str(e)})

    
@api_view(['POST'])
def get_battle_royal_matches_details(request):
    try:
        get_type = request.data['get_type']
        stage_id = request.data['stage_id']
        stage = Stage.objects.get(id = stage_id)
        battleRoyale = BattleRoyalMatch.objects.get(stage = stage)
        if get_type == "Team":
            match_details = BattleRoyalTeamDetails.objects.filter(battleRoyale = battleRoyale)
            match_details_serializer = BattleRoyalTeamDetailsSerializer(match_details, many = True)
            return Response({'status':200, "matches":match_details_serializer.data})
        elif get_type == "Player":
            match_player_details = BattleRoyalPlayerDetails.objects.filter(battleRoyale = battleRoyale)
            match_details_serializer = BattleRoyalPlayerDetailsSerializer(match_player_details, many = True)
            return Response({'status':200, "matches":match_details_serializer.data})
        
    except Exception as e:
        return Response({'status':500, "message":str(e)})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendEmailToBattleRoyaleTeamOrPlayers(request):
    try:
        data = request.data
        team_or_player_type = data['team_or_player_type']
        stage_id = data['stage_id']
        stage = Stage.objects.get(id = stage_id)
        battle_royal = BattleRoyalMatch.objects.get(stage = stage)
        receipent_lists = []
        if team_or_player_type == "Team":
            battle_royal_match_details = BattleRoyalTeamDetails.objects.filter(battleRoyale = battle_royal)
            battleRoyaleSerializer = BattleRoyalTeamDetailsSerializer(battle_royal_match_details, many = True)
            for team in battleRoyaleSerializer.data['teams']:
                team = Team.objects.get(id = team)
                teamSerializer = TeamSerializer(team, many = False)
                for p in teamSerializer.data['players']:
                    user = UserProfile.objects.get(id = p['id'])
                    receipent_lists.append(user.email)
        else:
            battle_royal_player_match_details = BattleRoyalTeamDetails.objects.filter(battleRoyale = battle_royal)
            battleRoyalePlayerMatchSerializer = BattleRoyalTeamDetailsSerializer(battle_royal_player_match_details, many = True)
            for player in battleRoyalePlayerMatchSerializer.data['players']:
                user = UserProfile.objects.get(id = player)
                receipent_lists.append(user.email)

        send_mail(
                    'ESSAN Credentials: Your Room Credentials',
                    f"Your room id is: {data['room_id']} and password is: {data['password']}",
                    'manishregmi39@gmail.com',
                    receipent_lists,
                    fail_silently=False,
                    )
        return Response({'status':200, "message":"Email sent successfully"})
    except Exception as e:
        return Response({'status':500, "message":str(e)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendAnnouncementEmailToTeams(request):
    try:    
        stage_id = request.POST.get('stage_id')
        stage = Stage.objects.get(id = stage_id)
        stageSerializer = StageSerializer(stage, many = False)
        tournament = Tournament.objects.get(slug=stageSerializer.data['tournament']['slug'])
        registrations = TeamTournamentRegistration.objects.filter(tournament=tournament)
        serializer = TeamTournamentRegistrationSerializer(registrations, many=True)
        for tournament_team in serializer.data:
            team = Team.objects.get(id = tournament_team['team']['id'])
            teamSerializer = TeamSerializer(team, many = False)
            for teamPlayer in teamSerializer.data['players']:
                player = UserProfile.objects.get(id= teamPlayer['id'])
                playerSerializerData = UserProfileSerializer(player, many = False)
                send_mail(
            'Announcement From Essan Gaming',
            request.data['message'],
            'manishregmi39@gmail.com',
            [playerSerializerData.data['email']],
            fail_silently=False,
        )
        return Response({
            "success":"Email sent to all players registered on the tournament."
        },status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'status':500, "message":str(e)})

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def getLeaderBoardData(request):
    try:
        stages_id = request.data['stages_id']
        leaderborad_type = request.data['leaderborad_type']
        leaderBoardDataLists = []
        if leaderborad_type == "Team":
            for stage_id in stages_id:
                stage = Stage.objects.get(id = stage_id)
                battleRoyalMatch = BattleRoyalMatch.objects.get(stage = stage)
                battleRoyalTeamDetails = BattleRoyalTeamDetails.objects.filter(battleRoyale = battleRoyalMatch)
                battleRoyalTeamDetailsSerializer = BattleRoyalTeamDetailsSerializer(battleRoyalTeamDetails, many = True)
                for d in battleRoyalTeamDetailsSerializer.data:
                    leaderBoardDataLists.append(d)

        elif leaderborad_type == "Player":
            for stage_id in stages_id:
                stage = Stage.objects.get(id = stage_id)
                battleRoyalMatch = BattleRoyalMatch.objects.get(stage = stage)
                battleRoyalPlayerDetails = BattleRoyalPlayerDetails.objects.filter(battleRoyale = battleRoyalMatch)
                battleRoyalPlayerDetailsSerializer = BattleRoyalPlayerDetailsSerializer(battleRoyalPlayerDetails, many = True)
                for d in battleRoyalPlayerDetailsSerializer.data:
                    leaderBoardDataLists.append(d)
        return Response({'status':200, "leaderBoardData":leaderBoardDataLists})
    
    except Exception as e:
        return Response({'status':500, "message":str(e)})


# send match room id password
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def sendAnnouncementEmailToMatchTeam(request):
    try:    
        team1 = request.POST.get('team1')
        team2 = request.POST.get('team2')
        roomId = request.POST.get('roomId')
        roomPassword = request.POST.get('roomPassword')
        team1Player = Team.objects.get(id = team1)
        team2Player = Team.objects.get(id = team2)
        team1Serializer = TeamSerializer(team1Player, many = False)
        team2Serializer = TeamSerializer(team2Player, many = False)
        for teamPlayer in team1Serializer.data['players']:
                player = UserProfile.objects.get(id= teamPlayer['id'])
                playerSerializerData = UserProfileSerializer(player, many = False)
                send_mail(
            'Essan Gaming: Credentials of your match room',
            f"Hello {playerSerializerData.data['username']}, \n Your room id: {roomId} \n Your password of room: {roomPassword} ",
            'manishregmi39@gmail.com',
            [playerSerializerData.data['email']],
            fail_silently=False,
        )
        for teamPlayer in team2Serializer.data['players']:
                player = UserProfile.objects.get(id= teamPlayer['id'])
                playerSerializerData = UserProfileSerializer(player, many = False)
                send_mail(
            'Essan Gaming: Credentials of your match room',
            f"Hello {playerSerializerData.data['username']}, \n Your room id: {roomId} \n Your password of room: {roomPassword} ",
            'manishregmi39@gmail.com',
            [playerSerializerData.data['email']],
            fail_silently=False,
        )
        
        return Response({'status':200, "message":"Room credentials sent to players"})
    
    except Exception as e:
        return Response({'status':500, "message":str(e)})


# calculate the number of rounds 
def calculate_rounds_matches(num_teams):
    try:
        # Calculate the number of rounds
        num_rounds = math.ceil(math.log2(num_teams))

        # Calculate the matches for each round
        matches_per_round = [num_teams // 2**round for round in range(num_rounds, 0, -1)]

        # Reverse the matches_per_round list
        matches_per_round.reverse()

        return num_rounds, matches_per_round
    except ValueError:
        return None
    
def generate_double_elimination_matches(participants):
    wb_rounds = 0
    wb_matches_per_round = []
    global_praticipants = participants
    
    while participants > 1:
        wb_rounds += 1
        wb_matches_per_round.append(participants // 2)
        participants = (participants + 1) // 2

    lb_rounds = wb_rounds - 1
    lb_matches_per_round = []

    # Calculating loser's bracket matches
    lb_participants = global_praticipants // 2
    while lb_participants > 1:
        lb_matches_per_round.append(lb_participants // 2)
        lb_participants = (lb_participants + 1) // 2

    return {
        "WB": [wb_rounds, wb_matches_per_round],
        "LB": [lb_rounds, lb_matches_per_round]
    }

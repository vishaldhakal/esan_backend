from .models import EliminationMode, Event, Stage,Team,Game, TeamTournamentRegistration, Tournament, TournamentFAQ, TournamentSponsor, TournamentStreams
from account.models import Organizer, Organization
from .serializers import StageSerializer, TeamTournamentRegistrationSerializer, TournamentFAQSerializer, TournamentSerializer, TournamentSponsorSerializer, TeamSerializer, TournamentStreamsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament(request):
    try:
        user = request.user
        # Check if the user is an organizer
        if user.role != "Organizer" or user.role != "Admin":
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
def tournaments_list(request):
    tournaments = Tournament.objects.filter(is_published=True)
    serializers = TournamentSerializer(tournaments, many=True)
    return Response({"tournaments": serializers.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_tournaments_list(request):
    user = request.user
    eslug = request.GET.get("slug")
    try:
        event = Event.objects.get(slug=eslug)
        orgg = Organizer.objects.get(user=user)
        tournaments = Tournament.objects.filter(organizer=orgg, event=event)
        serializers = TournamentSerializer(tournaments, many=True)
        return Response({"tournaments": serializers.data}, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_detail(request, id):
    tournament = Tournament.objects.get(id = id)
    tournament_serializer = TournamentSerializer(tournament)
    faq = TournamentFAQ.objects.filter(tournament = tournament)
    faq_serializer = TournamentFAQSerializer(faq, many = True)
    sponsor = TournamentSponsor.objects.filter(tournament = tournament)
    sponsor_serializer = TournamentSponsorSerializer(sponsor, many = True)
    return Response({
        'tournament': tournament_serializer.data,
        'faq': faq_serializer.data,
        'sponsor': sponsor_serializer.data
    })
   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_details(request):
    slug = request.GET.get("slug") 
    tournament = Tournament.objects.get(slug = slug)
    tournament_serializer = TournamentSerializer(tournament)
    return Response({
        'tournament': tournament_serializer.data,
    })
   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament(request):
    slug = request.POST.get("slug")
    
    tournament = Tournament.objects.get(slug=slug)
    user = request.user
    tournament_name = request.POST.get('tournament_name', tournament.tournament_name)
    tournament_logo = request.FILES.get('tournament_logo', None)
    tournament_banner = request.FILES.get('tournament_banner', None)
    location = request.POST.get('location', tournament.location)
    tournament_mode = request.POST.get('tournament_mode', tournament.tournament_mode)
    is_free = request.POST.get('is_free', tournament.is_free)
    tournament_fee = request.POST.get('tournament_fee', tournament.tournament_fee)
    maximum_no_of_participants = request.POST.get('maximum_no_of_participants', tournament.maximum_no_of_participants)
    tournament_description = request.POST.get('tournament_description', tournament.tournament_description)
    tournament_short_description = request.POST.get('tournament_short_description', tournament.tournament_short_description)
    tournament_rules = request.POST.get('tournament_rules', tournament.tournament_rules)
    tournament_prize_pool = request.POST.get('tournament_prize_pool', tournament.tournament_prize_pool)
    registration_opening_date = request.POST.get('registration_opening_date', tournament.registration_opening_date)
    registration_closing_date = request.POST.get('registration_closing_date', tournament.registration_closing_date)
    tournament_start_date = request.POST.get('tournament_start_date', tournament.tournament_start_date)
    tournament_end_date = request.POST.get('tournament_end_date', tournament.tournament_end_date)
    is_published = request.POST.get('is_published', tournament.is_published)
    is_registration_enabled = request.POST.get('is_registration_enabled', tournament.is_registration_enabled)
    accept_registration_automatic = request.POST.get('accept_registration_automatic', tournament.accept_registration_automatic)
    contact_email = request.POST.get('contact_email', tournament.contact_email)
    discord_link = request.POST.get('discord_link', tournament.discord_link)

    print(tournament_logo)

    if tournament.organizer.user != user or user.role!= "Admin":
        return Response({"error": "You are not authorized to update this Tournament"}, status=status.HTTP_403_FORBIDDEN)

    tournament.tournament_name = tournament_name
    if tournament_logo:
        tournament.tournament_logo = tournament_logo
    if tournament_banner:
        tournament.tournament_banner = tournament_banner
    tournament.tournament_mode = tournament_mode
    tournament.location = location
    tournament.is_free = is_free
    tournament.tournament_fee = tournament_fee
    tournament.maximum_no_of_participants = maximum_no_of_participants
    tournament.tournament_description = tournament_description
    tournament.tournament_short_description = tournament_short_description
    tournament.tournament_rules = tournament_rules
    tournament.tournament_prize_pool = tournament_prize_pool
    tournament.registration_opening_date = registration_opening_date
    tournament.registration_closing_date = registration_closing_date
    tournament.tournament_start_date = tournament_start_date
    tournament.tournament_end_date = tournament_end_date
    tournament.is_published = is_published
    tournament.is_registration_enabled = is_registration_enabled
    tournament.accept_registration_automatic = accept_registration_automatic
    tournament.contact_email = contact_email
    tournament.discord_link = discord_link

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
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
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
@permission_classes([IsAuthenticated])
def get_tournament_sponsor_list(request):
    tournament_sponsors = TournamentSponsor.objects.all()
    serializer = TournamentSponsorSerializer(tournament_sponsors, many=True)
    return Response({"tournament_sponsors": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_faq(request):
    slug = request.POST.get('slug')
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
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
@permission_classes([IsAuthenticated])
def get_tournament_faq_list(request):
    tournament_faqs = TournamentFAQ.objects.all()
    serializer = TournamentFAQSerializer(tournament_faqs, many=True)
    return Response({"tournament_faqs": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    user = request.user
    if user.role != "Organizer" and user.role != "Admin":
        return Response({"error": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
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
    if user.role == "Organizer" or user.role == "Admin":

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
@permission_classes([IsAuthenticated])
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

    if user.role == "Organizer" or user.role == "Admin":
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

    if user.role == "Organizer" or user.role == "Admin":
        tournament_stream = TournamentStreams.objects.get(id=stream_id)
        tournament_stream.delete()
        return Response({"success": "TournamentStream deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the tournament stream"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stage(request):
    user = request.user
    
    if user.role == "Organizer" or user.role == "Admin":
        elimination_mode_id = request.POST.get('elimination_mode_id')
        stage_number = request.POST.get('stage_number')
        no_of_participants = request.POST.get('no_of_participants')
        no_of_groups = request.POST.get('no_of_groups')
        stage_name = request.POST.get('stage_name')
        tournament_id = request.POST.get('tournament_id')

        try:
            elimination_mode = EliminationMode.objects.get(id=elimination_mode_id)
            tournament = Tournament.objects.get(id=tournament_id)
        except (EliminationMode.DoesNotExist, Tournament.DoesNotExist):
            return Response({"error": "Invalid elimination mode or tournament"}, status=status.HTTP_404_NOT_FOUND)
        stage = Stage.objects.create(
            stage_elimation_mode=elimination_mode,
            stage_number=stage_number,
            no_of_participants=no_of_participants,
            no_of_groups=no_of_groups,
            stage_name=stage_name,
            tournament=tournament
        )
        stage.save()
        return Response({"success": "Stage created successfully"})
        
    else:
        return Response({"error": "Unauthorized to create a stage"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
def update_stage(request):
    stage_id = request.GET.get('id')
    user = request.user

    if user.role == "Organizer" or user.role == "Admin":
        stage_number = request.POST.get('stage_number')
        no_of_participants = request.POST.get('no_of_participants')
        no_of_groups = request.POST.get('no_of_groups')
        stage_name = request.POST.get('stage_name')

        try:
            stage = Stage.objects.get(id=stage_id)
        except (Stage.DoesNotExist):
            return Response({"error": "Invalid stage"})
        stage.stage_number = stage_number
        stage.no_of_participants = no_of_participants
        stage.no_of_groups = no_of_groups
        stage.stage_name = stage_name
        stage.save()
        return Response({"success": "Stage updated successfully"})
    
    else:
        return Response({"error": "Unauthorized to update the stage"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stage(request):
    stage_id = request.GET.get("id")
    user = request.user

    if user.role == "Organizer" or user.role == "Admin":
        try:
            stage = Stage.objects.get(id=stage_id)
        except Stage.DoesNotExist:
            return Response({"error": "Stage not found"})
        stage.delete()
        return Response({"success": "Stage deleted successfully"})
        
    else:
        return Response({"error": "Unauthorized to delete the stage"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def registered_teams(request):
    slug = request.GET.get("slug")
    
    user = request.user

    if user.role == "Organizer" or user.role == "Admin":
        tournament = Tournament.objects.get(slug=slug)
        registrations = TeamTournamentRegistration.objects.filter(tournament__in=tournament)
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

    is_free = bool(request.POST.get('is_free',False)) 
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

    if tournament.registration_opening_date and tournament.tournament_start_date:
        if tournament.registration_opening_date >= tournament.tournament_start_date:
            return Response({"error": "Registration opening date must be before the tournament start date"}, status=status.HTTP_400_BAD_REQUEST)

    if tournament.registration_closing_date and tournament.tournament_start_date:
        if tournament.registration_closing_date >= tournament.tournament_start_date:
            return Response({"error": "Registration closing date must be before the tournament start date"}, status=status.HTTP_400_BAD_REQUEST)

    if tournament.registration_opening_date and tournament.registration_closing_date:
        if tournament.registration_opening_date >= tournament.registration_closing_date:
            return Response({"error": "Registration opening date must be before the registration closing date"}, status=status.HTTP_400_BAD_REQUEST)

    tournament.save()

    return Response({"success": "Registration opened for the tournament"})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def register_team_initials(request):
    user = request.user
    orgg = Organization.objects.get(user=user)
    tournament_id = request.GET.get('tournament_id')
    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except (Tournament.DoesNotExist, Team.DoesNotExist):
        return Response({"error": "Invalid tournament or team"}, status=404)

    gam = tournament.game
    teamss = Team.objects.filter(organization=orgg,game=gam)
    teamss_ser = TeamSerializer(teamss,many=True)
    return Response({"teamss": teamss_ser.data})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_team(request):
    user = request.user
    tournament_id = request.POST.get('tournament_id')
    team_id = request.POST.get('team_id')
    registration_fee = request.POST.get('registration_fee')
    registration_status = request.POST.get('registration_status', 'Ongoing Review')
    payment_method = request.POST.get('payment_method', 'Other')

    try:
        tournament = Tournament.objects.get(id=tournament_id)
        team = Team.objects.get(id=team_id)
    except (Tournament.DoesNotExist, Team.DoesNotExist):
        return Response({"error": "Invalid tournament or team"}, status=404)

    if user.role == "Organization" or user.role == "Admin":
            registration = TeamTournamentRegistration.objects.create(
                tournament=tournament,
                team=team,
                registration_fee=registration_fee,
                registration_status=registration_status,
                payment_method=payment_method,
            )
            registration.save()
            return Response({"success": "Team registered successfully"})
    else:
        return Response({"error": "Unauthorized to register a team"})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_team_registration(request):
    registration_id = request.GET.get('id')
    user = request.user

    if user.role == "Organization" or user.role == "Admin":
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

    if user.role == "Organization" or "Admin":
        try:
            team_registration = TeamTournamentRegistration.objects.get(id=registration_id)
        except TeamTournamentRegistration.DoesNotExist:
            return Response({"error": "Team registration not found"})
        team_registration.delete()
        return Response({"success": "Team registration deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the team registration"}, status=status.HTTP_401_UNAUTHORIZED)
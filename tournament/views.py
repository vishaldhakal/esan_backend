
# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from account.models import Organizer
# from account.serializers import GameSerializer
# from .models import BannerImage, Game, PrizePool, Sponsor, Team, Tournament, Registration, Participant, LivePage, Announcement, Match, TournamentBracket
# from .serializers import BannerImageSerializer, PrizePoolSerializer, SponsorSerializer, TeamSerializer, TournamentBracketSerializer, TournamentSerializer, RegistrationSerializer, MatchSerializer, ParticipantSerializer, LivePageSerializer, AnnouncementSerializer
# from rest_framework import status

# @api_view(['GET'])
# def sponsor_list(request):
#     sponsors = Sponsor.objects.all()
#     serializer = SponsorSerializer(sponsors, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def sponsor_detail(request, pk):
#     sponsor = get_object_or_404(Sponsor, pk=pk)
#     serializer = SponsorSerializer(sponsor)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_tournament(request):
#     name = request.data.get('name')
#     description = request.data.get('description')
#     start_date = request.data.get('start_date')
#     end_date = request.data.get('end_date')
#     location = request.data.get('location')
#     rules = request.data.get('rules')
#     organizer_id = request.data.get('organizer_id')
#     try:
#         organizer = Organizer.objects.get(pk=organizer_id)
#         tournament = Tournament.objects.create(
#             name=name,
#             description=description,
#             start_date=start_date,
#             end_date=end_date,
#             location=location,
#             rules=rules,
#             organizer=organizer
#         )
#         data = {
#             'id': tournament.id,
#             'name': tournament.name,
#             'description': tournament.description,
#             'start_date': tournament.start_date,
#             'end_date': tournament.end_date,
#             'location': tournament.location,
#             'rules': tournament.rules,
#             'organizer': tournament.organizer.user
#         }
#         return Response(data, status=201)
#     except Organizer.DoesNotExist:
#         return Response({'error': 'Organizer not found.'})
    
# @api_view(['PUT'])
# def update_tournament(request, pk):
#     try:
#         tournament = Tournament.objects.get(pk=pk)
#         name = request.data.get('name')
#         description = request.data.get('description')
#         start_date = request.data.get('start_date')
#         end_date = request.data.get('end_date')
#         location = request.data.get('location')
#         rules = request.data.get('rules')
#         organizer_id = request.data.get('organizer_id')
#         try:
#             organizer = Organizer.objects.get(pk=organizer_id)
#             tournament.name = name
#             tournament.description = description
#             tournament.start_date = start_date
#             tournament.end_date = end_date
#             tournament.location = location
#             tournament.rules = rules
#             tournament.organizer = organizer
#             tournament.save()
#             data = {
#                 'id': tournament.id,
#                 'name': tournament.name,
#                 'description': tournament.description,
#                 'start_date': tournament.start_date,
#                 'end_date': tournament.end_date,
#                 'location': tournament.location,
#                 'rules': tournament.rules,
#                 'organizer': tournament.organizer.user
#             }
#             return Response(data)
#         except Organizer.DoesNotExist:
#             return Response({'error': 'Organizer not found.'})
#     except Tournament.DoesNotExist:
#         return Response({'error': 'Tournament not found.'})

# @api_view(['DELETE'])
# def delete_tournament(request, pk):
#     try:
#         tournament = Tournament.objects.get(pk=pk)
#     except Tournament.DoesNotExist:
#         return Response({'message': 'The tournament does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     if request.user != tournament.organizer.user:
#         return Response({'message': 'You are not authorized to delete this tournament'},
#                         status=status.HTTP_401_UNAUTHORIZED)

#     tournament.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def tournament_list(request):
#     tournaments = Tournament.objects.all()
#     data = []
#     for tournament in tournaments:
#         data.append({
#             'id': tournament.id,
#             'name': tournament.name,
#             'description': tournament.description,
#             'start_date': tournament.start_date,
#             'end_date': tournament.end_date,
#             'location': tournament.location,
#             'organizer': tournament.organizer.user
#         })
#     return Response(data)

# @api_view(['GET'])
# def tournament_detail(request, pk):
#     try:
#         tournament = Tournament.objects.get(pk=pk)
#         data = {
#             'id': tournament.id,
#             'name': tournament.name,
#             'description': tournament.description,
#             'start_date': tournament.start_date,
#             'end_date': tournament.end_date,
#             'location': tournament.location,
#             'organizer': tournament.organizer.user
#         }
#         return Response(data)
#     except Tournament.DoesNotExist:
#         return Response({'error': 'Tournament not found.'})

# @api_view(['GET', 'POST'])
# def team_list(request):
#     if request.method == 'GET':
#         teams = Team.objects.all()
#         serializer = TeamSerializer(teams, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = TeamSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def team_detail(request, pk):
#     try:
#         team = Team.objects.get(pk=pk)
#     except Team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = TeamSerializer(team)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = TeamSerializer(team, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         team.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def prizepool_list(request):
#     prizepools = PrizePool.objects.all()
#     serializer = PrizePoolSerializer(prizepools, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def prizepool_detail(request, pk):
#     try:
#         prizepool = PrizePool.objects.get(pk=pk)
#     except PrizePool.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = PrizePoolSerializer(prizepool)
#     return Response(serializer.data)

# @api_view(['POST'])
# def prizepool_create(request):
#     serializer = PrizePoolSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def prizepool_update(request, pk):
#     try:
#         prizepool = PrizePool.objects.get(pk=pk)
#     except PrizePool.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = PrizePoolSerializer(prizepool, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def prizepool_delete(request, pk):
#     try:
#         prizepool = PrizePool.objects.get(pk=pk)
#     except PrizePool.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     prizepool.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def bannerimage_list(request):
#     bannerimages = BannerImage.objects.all()
#     serializer = BannerImageSerializer(bannerimages, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def bannerimage_create(request):
#     serializer = BannerImageSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def bannerimage_update(request, pk):
#     try:
#         bannerimage = BannerImage.objects.get(pk=pk)
#     except BannerImage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = BannerImageSerializer(bannerimage, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def bannerimage_delete(request, pk):
#     try:
#         bannerimage = BannerImage.objects.get(pk=pk)
#     except BannerImage.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     bannerimage.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def game_list(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         serializer = GameSerializer(games, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = GameSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def game_detail(request, pk):
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = GameSerializer(game)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = GameSerializer(game, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         game.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['POST'])
# def create_registration(request):
#     serializer = RegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['PUT'])
# def update_registration(request, pk):
#     registration = get_object_or_404(Registration, pk=pk)
#     serializer = RegistrationSerializer(registration, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def delete_registration(request, pk):
#     registration = get_object_or_404(Registration, pk=pk)
#     registration.delete()
#     return Response(status=204)

# @api_view(['POST'])
# def create_participant(request):
#     serializer = ParticipantSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def delete_participant(request, pk):
#     participant = get_object_or_404(Participant, pk=pk)
#     participant.delete()
#     return Response(status=204)

# @api_view(['GET'])
# def match_detail(request, pk):
#     match = get_object_or_404(Match, pk=pk)
#     serializer = MatchSerializer(match)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_match(request):
#     serializer = MatchSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['PUT'])
# def update_match(request, pk):
#     match = get_object_or_404(Match, pk=pk)
#     serializer = MatchSerializer(match, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def delete_match(request, pk):
#     match = get_object_or_404(Match, pk=pk)
#     match.delete()
#     return Response(status=204)


# @api_view(['GET', 'POST'])
# def tournament_bracket_list(request):
#     """
#     List all tournament brackets, or create a new bracket.
#     """
#     if request.method == 'GET':
#         brackets = TournamentBracket.objects.all()
#         serializer = TournamentBracketSerializer(brackets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = TournamentBracketSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def tournament_bracket_detail(request, pk):
#     """
#     Retrieve, update or delete a tournament bracket.
#     """
#     bracket = get_object_or_404(TournamentBracket, pk=pk)

#     if request.method == 'GET':
#         serializer = TournamentBracketSerializer(bracket)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = TournamentBracketSerializer(bracket, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         bracket.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def livepage_detail(request, pk):
#     livepage = get_object_or_404(LivePage, pk=pk)
#     serializer = LivePageSerializer(livepage)
#     return Response(serializer.data)

# @api_view(['PUT'])
# def update_livepage(request, pk):
#     livepage = get_object_or_404(LivePage, pk=pk)
#     serializer = LivePageSerializer(livepage, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['GET'])
# def announcement_detail(request, pk):
#     announcement = get_object_or_404(Announcement, pk=pk)
#     serializer = AnnouncementSerializer(announcement)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_announcement(request):
#     serializer = AnnouncementSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

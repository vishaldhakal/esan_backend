from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import *
from tournament.models import Team,Game
from tournament.serializers import GameSerializer,TeamOrgSerializer
from .serializers import UserProfileDetailSerializer,PlayerSerializer,BlogWritterSerializer,OrganizerSerializer,OrganizationSerializer,ChangePasswordSerializer,PlayerRequestSerializer,UserProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import generics
import random
from django.shortcuts import redirect
from django.urls import reverse

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user":{
                'user': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }   
        },status=200)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = UserProfile
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_user_profile(request):
    userid = request.GET.get("user")
    userpr = UserProfile.objects.get(id=userid)
    userpr.is_verified = True
    userpr.save()
    redirect_uri = 'http://localhost:8081'
    return redirect(reverse(redirect_uri))
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile_detail(request):
    user = request.user
    users_ser = UserProfileDetailSerializer(user)
    return Response({
        'user': users_ser.data,
    },status=200)

@api_view(['POST'])
def create_user_profile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    user_type = request.POST.get('user_type', "is_player")

    # Check if email already exists
    if UserProfile.objects.filter(email=email).exists():
        return Response({'detail': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username already exists
    if UserProfile.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if all required fields are present
    if not all([first_name, last_name, email, password, username, user_type]):
        return Response({'detail': 'All required fields are not present'}, status=status.HTTP_400_BAD_REQUEST)

    if user_type=="is_player":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Player')
        player = Player.objects.create(user=user)   
        player.save()
        message = f'Hello,\n\nThank you for signing up for ESAN! To get started, please click on the following link to verify your account : https://jellyfish-app-dyg5s.ondigitalocean.app/api/verify-user-profile/?user={user.id} \n\nBest regards,\nESAN'

        send_mail(
        'Verify Your ESAN Account',
        message,
        'manavkhadka0@gmail.com',
        [email],
        fail_silently=False,
    )
        return Response({
        "success":"User Created Sucessfully"
    },status=status.HTTP_201_CREATED)

    elif user_type=="is_blog_writer":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Blog Writer')
        blog_writer = BlogWriter.objects.create(user=user)
        blog_writer.save()

    elif user_type=="is_organizer":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Organizer')
        organizer = Organizer.objects.create(user=user)
        organizer.save()

    elif user_type=="is_organization":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Organization')
        organization_name = request.POST['organization_name']
        organization = Organization.objects.create(user=user, organization_name=organization_name)
        organization.save()

    message = f'Hello,\n\nThank you for signing up for ESAN!\n\nBest regards,\nESAN'

    send_mail(
        'Thankyou for Registration',
        message,
        'manavkhadka0@gmail.com',
        [email],
        fail_silently=False,
    )
    return Response({
        "success":"User Created Sucessfully"
    },status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    if user.is_verified:
        data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            }
        }

        if user.role == 'Player':
            player = Player.objects.get(user=user)
            data['player'] = {
                'id': player.id,
                'nationality': player.user.nationality,
                'phone_number': player.user.phone_number
            }

        elif user.role == 'Blog Writer':
            blog_writer = BlogWriter.objects.get(user=user)
            data['blog_writer'] = {
                'id': blog_writer.id,
                'bio': blog_writer.user.bio,
                'website': blog_writer.user.website_link
            }

        elif user.role == 'Organizer':
            try:
                organizer = Organizer.objects.get(user=user)
                data['organizer'] = {
                'id': organizer.id,
                'organizer_name': organizer.organizer_name,
                'description': organizer.user.bio,
                'website': organizer.user.website_link,
                'address': organizer.user.address
                }
            except Organizer.DoesNotExist:
               return Response({'message':"organizer doesnot exists"}, status=status.HTTP_400_BAD_REQUEST)
               

        elif user.role == 'Organization':
            organization = Organization.objects.get(user=user)
            data['organization'] = {
                'id': organization.id,
                'organization_name': organization.organization_name,
                'bio': organization.user.bio,
                'website_link': organization.user.website_link,
                'address': organization.user.address
            }

        return Response(data,status=200)
    else:
        return Response({"detail":"User not verified"},status=403)

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_players(request):
    user = request.user
    try:
        organization = Organization.objects.get(user=user)
        players = organization.players.all()
        teams = Team.objects.filter(organization=organization)
        teams_ser = TeamOrgSerializer(teams,many=True)
        free_players = players.exclude(id__in=teams.values('players'))
        free_players_ser = UserProfileSerializer(free_players,many=True)
        return Response({"free_players":free_players_ser.data,"teams":teams_ser.data}, status=201)
    except:
        return Response({"error":"Organization Doesnot Exists"},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_players(request):
    try:
        userr = request.user
        players = UserProfile.objects.filter(role="Player")
        teams = Team.objects.all()
        organizations = Organization.objects.all()
        orgg = Organization.objects.get(user=userr)
        playerreqs = PlayerRequest.objects.filter(organization=orgg,request_status="Requested").values_list("player")
        all_prss = PlayerRequest.objects.filter(organization=orgg)
        all_prss_ser = PlayerRequestSerializer(all_prss,many=True)
        free_players = players.exclude(id__in=teams.values('players')).exclude(id__in=organizations.values_list('players')).exclude(id__in=playerreqs)
        free_players_ser = UserProfileSerializer(free_players,many=True)
        return Response({"free_players":free_players_ser.data,"player_requests":all_prss_ser.data}, status=201)
    except:
        return Response({"error":"Problem fetching Players"},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_organizations(request):
    try:
        organizations = Organization.objects.all()
        user = request.user
        if user.role == "Player":
            player_requests = PlayerRequest.objects.filter(player=user,request_status="Requested")
            player_requests2 = PlayerRequest.objects.filter(player=user,request_status="Requested").values_list("organization")
            player_requests_ser = PlayerRequestSerializer(player_requests,many=True)
            organizations = Organization.objects.exclude(players=user)
            orgs = organizations.exclude(id__in=player_requests2)
            organizations_ser = OrganizationSerializer(orgs,many=True)
            return Response({"player_requests":player_requests_ser.data,"free_organizations":organizations_ser.data},status=status.HTTP_200_OK)
        elif user.role == "Organization":
            orgg = Organization.objects.get(user=user)
            player_requests = PlayerRequest.objects.filter(organization=orgg,request_status="Requested")
            player_requests_ser = PlayerRequestSerializer(player_requests,many=True)
            organizations_ser = OrganizationSerializer(organizations,many=True)
            return Response({"player_requests":player_requests_ser.data,"free_organizations":organizations_ser.data},status=status.HTTP_200_OK)
    except:
        return Response({"error":"Problem fetching organizations"},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_player(request):
    user = request.user
    if user.role == "Player":
        orgid = request.GET.get("id")
        org = Organization.objects.get(id=orgid)
        newpr = PlayerRequest.objects.create(player=user,organization=org,request_started_by="Player",request_status="Requested")
        newpr.save()
        return Response({"success":"Player request success"},status=status.HTTP_201_CREATED)
    elif user.role == "Organization":
        plaid = request.GET.get("id")
        player = UserProfile.objects.get(id=plaid)
        orgg = Organization.objects.get(user=user)
        newpr = PlayerRequest.objects.create(organization=orgg,player=player,request_started_by="Organization",request_status="Requested")
        newpr.save()
        return Response({"success":"Player request success"},status=status.HTTP_201_CREATED)
    else:
        return Response({"error":"You cannot request"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_requests(request):
    user = request.user
    if user.role == "Player":
        player_requests = PlayerRequest.objects.filter(player=user,request_status="Requested")
        player_requests_ser = PlayerRequestSerializer(player_requests,many=True)
        return Response({"player_requests":player_requests_ser.data},status=status.HTTP_200_OK)
    elif user.role == "Organization":
        orgg = Organization.objects.get(user=user)
        player_requests = PlayerRequest.objects.filter(organization=orgg,request_status="Requested")
        player_requests_ser = PlayerRequestSerializer(player_requests,many=True)
        return Response({"player_requests":player_requests_ser.data},status=status.HTTP_200_OK)
    else:
        return Response({"error":"You cannot request"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request):
    user = request.user
    reqid = request.GET.get("id")
    remarks = request.POST.get("remarks"," ")
    player_request = PlayerRequest.objects.get(id=reqid)
    orgg = player_request.organization
    player = player_request.player
    orgg.players.add(player)
    orgg.save()
    player_request.request_status = "Accepted"
    player_request.remarks = remarks
    player_request.save()
    return Response({"success":"Request Accepted"},status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_request(request):
    reqid = request.GET.get("id")
    player_request = PlayerRequest.objects.get(id=reqid)
    player_request.delete()
    return Response({"success":"Deleted Sucessfully"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_request(request):
    user = request.user
    reqid = request.GET.get("id")
    remarks = request.POST.get("remarks"," ")
    player_request = PlayerRequest.objects.get(id=reqid)
    player_request.request_status = "Rejected"
    player_request.remarks = remarks
    player_request.save()
    return Response({"success":"Request Rejected"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_users(request):
    users = UserProfile.objects.all()
    users_serializer = UserProfileDetailSerializer(users,many=True)
    return Response({"users":users_serializer.data},status=200)

@api_view(['GET'])
def get_user_detail(request):
    username = request.GET.get("name")
    user = UserProfile.objects.get(username=username)
    users_serializer = UserProfileDetailSerializer(user)

    if user.role == "Player":
        player = Player.objects.get(user=user)
        player_serializer = PlayerSerializer(player)
        return Response({"user":users_serializer.data,"detail":player_serializer.data},status=200)
    elif user.role == "Blog Writer":
        blog_writer = BlogWriter.objects.get(user=user)
        blog_writer_serializer = BlogWritterSerializer(blog_writer)
        return Response({"user":users_serializer.data,"detail":blog_writer_serializer.data},status=200)
    elif user.role == "Organization":
        organization = Organization.objects.get(user=user)
        organization_serializer = OrganizationSerializer(organization)
        return Response({"user":users_serializer.data,"detail":organization_serializer.data},status=200)
    elif user.role == "Organizer":
        organizer = Organizer.objects.get(user=user)
        organizer_serializer = OrganizerSerializer(organizer)
        return Response({"user":users_serializer.data,"detail":organizer_serializer.data},status=200)
    else:
        return Response({"user":users_serializer.data},status=200)

@api_view(['POST'])
def update_user_detail(request):
    username = request.POST.get("username")
    user = UserProfile.objects.get(username=username)

    user.first_name = request.POST.get("first_name")
    user.last_name = request.POST.get("last_name")
    user.nationality = request.POST.get("nationality","Nepal")
    user.phone_number = request.POST.get("phone_number"," ")
    user.address = request.POST.get("address", " ")
    user.bio = request.POST.get("bio"," ")
    user.status = request.POST.get("status","Active")
    user.is_verified = request.POST.get("is_verified","False")=="True"
    user.role = request.POST.get("role")
    user.avatar = request.FILES.get("avatar")
    
    user.facebook_link = request.POST.get("facebook_link"," ")
    user.instagram_link = request.POST.get("instagram_link"," ")
    user.twitch_link = request.POST.get("twitch_link"," ")
    user.discord_link = request.POST.get("discord_link"," ")
    user.reddit_link = request.POST.get("reddit_link"," ")
    user.website_link = request.POST.get("website_link"," ")
    user.youtube_link = request.POST.get("youtube_link"," ")
    user.twitter_link = request.POST.get("twitter_link"," ")
    user.linkedin_link = request.POST.get("linkedin_link"," ")

    user.save()

    return Response({"success":"Updated sucess"},status=200)

@api_view(['POST'])
def checkEmail(request):
    try:
        user = UserProfile.objects.filter(email = request.data['email']).exists()
        if not user:
         return Response({'status':400, 'message':'No user found'})
        finaluser = UserProfile.objects.get(email = request.data['email']).id
        random_float = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        checkOtp = OTP.objects.filter(user = finaluser).exists()
        if checkOtp:
            otp = OTP.objects.get(user = finaluser)
            otp.otp = random_float
            otp.save()
            send_mail(
        'Essan OTP Verification',
        'Here is your otp.' + str(random_float),
        'manavkhadka0@gmail.com',
        [request.data['email']],
        fail_silently=False,
    )
            return Response({'status':200, "message":"OTP sent successfully"})
        else:
            otp = OTP.objects.create(
                user = UserProfile.objects.get(email = request.data['email']),
                otp = random_float,
            )
            send_mail(
        'Essan verification',
        'Here is your otp.' + str(random_float),
        'manavkhadka0@gmail.com',
        [request.data['email']],
        fail_silently=False,
    )
            return Response({'status':200})
    
    except Exception as e:
            return Response({'message':str(e)})


@api_view(['POST'])
def checkOtpAndChangePassword(request):
    user = UserProfile.objects.get(email = request.data['email']).id
    otp = OTP.objects.get(user = user).otp
    if str(otp) == request.data['otp']:
        user = UserProfile.objects.get(email = request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        return Response({'status': 200, "message":"Password changed successfully"})
    else:
        return Response({'status':500, "message":'OTP did not matched'})



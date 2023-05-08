from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import BlogWriter, Game, Organization, Organizer, Player, UserProfile
from rest_framework import status
from .serializers import GameSerializer,UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
# from django.conf import settings
from esan_backend import settings



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
        })

@api_view(['POST'])
def CreateUserProfile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    user_type = request.POST.get('user_type', "is_player")

    if user_type=="is_player":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Player') 
        player = Player.objects.create(user=user)   
        player.save()

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

    return Response({
        "success":"User Created Sucessfully"
    },status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateUserProfile(request):
    user = request.user
    if user.is_verified:
        first_name = request.data.get('first_name', user.first_name)
        last_name = request.data.get('last_name', user.last_name)
        password = request.data.get('password', None)
        user_type = request.data.get('user_type', user.role)

        if user_type != user.role:
            # Update user type
            if user_type == 'Player':
                player = Player.objects.get_or_create(user=user)
                player.save()
            elif user_type == 'Blog Writer':
                blog_writer = BlogWriter.objects.get_or_create(user=user)
                blog_writer.save()
            elif user_type == 'Organizer':
                organizer = Organizer.objects.get_or_create(user=user)
                organizer.save()
            elif user_type == 'Organization':
                organization = Organization.objects.get_or_create(user=user)
                organization.save()

            user.role = user_type
            user.save()

        if password is not None:
            user.set_password(password)
            user.save()

        # Update UserProfile fields
        if user.role == 'Player':
            player = user.player
            player.country = request.data.get('country', player.country)
            player.phone_number = request.data.get('phone_number', player.phone_number)
            player.profile_picture = request.data.get('profile_picture', player.profile_picture)
            player.save()

        elif user.role == 'Blog Writer':
            blog_writer = user.blogwriter
            blog_writer.bio = request.data.get('bio', blog_writer.bio)
            blog_writer.profile_picture = request.data.get('profile_picture', blog_writer.profile_picture)
            blog_writer.website = request.data.get('website', blog_writer.website)
            blog_writer.save()

        elif user.role == 'Organizer':
            organizer = user.organizer
            organizer.logo = request.data.get('logo', organizer.logo)
            organizer.description = request.data.get('description', organizer.description)
            organizer.website = request.data.get('website', organizer.website)
            organizer.save()

        elif user.role == 'Organization':
            organization = user.organization
            organization.organization_name = request.data.get('organization_name', organization.organization_name)
            organization.logo = request.data.get('logo', organization.logo)
            organization.description = request.data.get('description', organization.description)
            organization.website = request.data.get('website', organization.website)
            organization.address = request.data.get('address', organization.address)
            organization.save()

        return Response({
            "success": "User Profile Updated Successfully"
        }, status=status.HTTP_200_OK)

    else:
        return Response({"detail":"User not verified"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserProfile(request):
    user = request.user
    if user.is_verified:
        data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'password_reset_token': user.password_reset_token if hasattr(user, 'userprofile') else None,

            }
        }

        if user.role == 'Player':
            player = Player.objects.get(user=user)
            data['player'] = {
                'id': player.id,
                'profile_picture': player.profile_picture.url if player.profile_picture else None,
                'country': player.country,
                'phone_number': player.phone_number
            }

        elif user.role == 'Blog Writer':
            blog_writer = BlogWriter.objects.get(user=user)
            data['blog_writer'] = {
                'id': blog_writer.id,
                'bio': blog_writer.bio,
                'profile_picture': blog_writer.profile_picture.url if blog_writer.profile_picture else None,
                'website': blog_writer.website
            }

        elif user.role == 'Organizer':
            organizer = Organizer.objects.get(user=user)
            data['organizer'] = {
                'id': organizer.id,
                'logo': organizer.logo.url if organizer.logo else None,
                'description': organizer.description,
                'website': organizer.website
            }

        elif user.role == 'Organization':
            organization = Organization.objects.get(user=user)
            data['organization'] = {
                'id': organization.id,
                'organization_name': organization.organization_name,
                'logo': organization.logo.url if organization.logo else None,
                'description': organization.description,
                'website': organization.website,
                'address': organization.address
            }

        return Response(data)
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


@api_view(['GET', 'POST'])
def GetUsers(request):
    users = UserProfile.objects.all()
    users_serializer = UserProfileSerializer(users,many=True)
    return Response({"users":users_serializer.data})


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({"detail": "Please provide an email"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"detail": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Generate the token and send reset password email
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    reset_password_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

    send_mail(
        'Reset your password',
        f'Click on the link to reset your password: {reset_password_link}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return Response({"detail": "Reset password link has been sent to your email."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"detail": "Please provide a new password"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "The reset password link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_email(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_verified = True
        user.save()

        return Response({"detail": "Email verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)

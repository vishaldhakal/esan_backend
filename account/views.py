from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import UserProfile

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
    
@api_view(['POST'])
def CreateUserProfile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    is_player = request.POST.get('is_player',False) == True
    is_organization = request.POST.get('is_organization',False) == True
    is_organizer = request.POST.get('is_organizer',False) == True
    is_blog_writer = request.POST.get('is_blog_writer',False) == True
    is_admin = request.POST.get('is_admin', False) == True

    # Create a new User object
    user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)

    # Create a new UserProfile object
    user_profile = UserProfile.objects.create(user=user, is_player=is_player, is_organization=is_organization, is_organizer=is_organizer, is_blog_writer=is_blog_writer)

    # Generate a new token for the user
    token, created = Token.objects.get_or_create(user=user)

    # Return a response with the token
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })
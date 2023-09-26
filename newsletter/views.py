from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Newsletter
from rest_framework import status

@api_view(["POST"])
def subscribe_newsletter(request):
    email = request.POST.get('email')
    newsletter = Newsletter.objects.create(
        email=email,
    )
    newsletter.save()
    # Send Email to user here
    return Response({"success":"Subscribed Sucessfully"},status=status.HTTP_200_OK)

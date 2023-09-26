
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Testimonial
from .serializers import TestimonialSerializer
from account.models import UserProfile

@api_view(['GET'])
def all_testimonials(request):
    testimonial = Testimonial.objects.all()
    testimonial_ser = TestimonialSerializer(testimonial,many=True)
    return Response({"testimonials": testimonial_ser.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def testimonials(request):
    testimonial = Testimonial.objects.filter(is_verified=True)
    testimonial_ser = TestimonialSerializer(testimonial,many=True)
    return Response({"testimonials": testimonial_ser.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_testimonial(request):
    user = request.user
    description = request.POST.get("description")
    rating = int(request.POST.get("rating"))
    testimonial = Testimonial(user=user,description=description,rating=rating)
    testimonial.save()
    return Response({"success": "Submitted Sucessfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_testimonial(request):
    idd = int(request.GET.get("id"))
    user = request.user
    if user.role == "Admin":
        testimonial = Testimonial.objects.get(id=idd)
        aaaa = testimonial.is_verified
        testimonial.is_verified = not aaaa
        testimonial.save()
        return Response({"success": "Submitted Sucessfully"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_testimonial(request):
    idd = int(request.GET.get("id"))
    user = request.user
    if user.role == "Admin":
        testimonial = Testimonial.objects.get(id=idd)
        testimonial.delete()
        return Response({"success": "Deleted Sucessfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_testimonial(request):
    idd = int(request.GET.get("id"))
    testimonial = Testimonial.objects.get(id=idd)
    description = request.POST.get("description")
    rating = int(request.POST.get("rating"))
    
    testimonial.description = description
    testimonial.rating = rating

    testimonial.save()
    return Response({"success": "Updated Sucessfully"}, status=status.HTTP_200_OK)
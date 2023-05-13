
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Testimonial
from .serializers import TestimonialSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_testimonial(request):
    user = request.POST['user']
    description = request.POST['description']
    rating =request.POST['rating']

    testimonial = Testimonial(
        user = user,
        description = description,
        rating = rating
    )
    testimonial.save()
    return Response({"Testimonial created successfully"})
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_testimonials(request):
    testimonials = Testimonial.objects.all()
    serializer = TestimonialSerializer(testimonials, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_testimonial(request, id):
    testimonial = Testimonial.objects.get(id=id)
    serializer = TestimonialSerializer(testimonial)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def edit_testimonial(request, id):
    testimonial = Testimonial.objects.get(id=id)
    user = request.POST.get('user')
    description = request.POST.get('description')
    rating =request.POST.get('rating')

    testimonial.user = user
    testimonial.description = description
    testimonial.rating = rating

    testimonial.save()
    return Response({"Testimonial Updated Successfully"})
    

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_testimonial(request, pk):
    testimonial = Testimonial.objects.get(pk=pk)
    testimonial.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
 
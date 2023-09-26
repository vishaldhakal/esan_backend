from rest_framework import serializers
from .models import Testimonial
from account.serializers import UserProfileSerializer

class TestimonialSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Testimonial
        fields = '__all__'

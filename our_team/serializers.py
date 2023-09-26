from rest_framework import serializers
from .models import OurTeam

class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = '__all__'

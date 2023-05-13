from rest_framework import serializers
from .models import OurTeam

class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = ['id', 'name', 'post']

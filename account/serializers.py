from rest_framework import serializers
from .models import Player, BlogWriter, Organization, Organizer,UserProfile,PlayerRequest

class ChangePasswordSerializer(serializers.Serializer):
    model = UserProfile
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','username','first_name','email','last_name','avatar','role','is_verified','status','phone_number','address','nationality','bio', 'facebook_link', 'instagram_link', 'twitch_link', 'discord_link', 'reddit_link', 'website_link', 'youtube_link', 'twitter_link', 'linkedin_link')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','username','first_name','last_name','avatar','email')

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class BlogWritterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogWriter
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Organizer
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Organization
        fields = '__all__'

class PlayerRequestSerializer(serializers.ModelSerializer):
    player = UserProfileSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    
    class Meta:
        model = PlayerRequest
        fields = '__all__'
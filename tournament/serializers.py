
# from rest_framework import serializers
# from .models import BannerImage, Match, PrizePool, Result, Sponsor, Team, Tournament, Registration, Participant, LivePage, Announcement, TournamentBracket
# from account.serializers import OrganizationSerializer, OrganizerSerializer, PlayerSerializer

# class SponsorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sponsor
#         fields = '__all__'

# class TournamentSerializer(serializers.ModelSerializer):
#     organizer = OrganizerSerializer()
#     sponsors = SponsorSerializer(many=True)

#     class Meta:
#         model = Tournament
#         fields = '__all__'

#     # def create(self, validated_data):
#     #     organizer_data = validated_data.pop('organizer')
#     #     sponsors_data = validated_data.pop('sponsors')
#     #     tournament = Tournament.objects.create(**validated_data)
#     #     organizer = Organizer.objects.create(tournament=tournament, **organizer_data)
#     #     sponsors = [Sponsor.objects.create(tournament=tournament, **sponsor_data) for sponsor_data in sponsors_data]
#     #     tournament.sponsors.set(sponsors)
#     #     return tournament

# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'

# class RegistrationSerializer(serializers.ModelSerializer):
#     captain = PlayerSerializer()
#     players = PlayerSerializer(many=True)
#     tournament = TournamentSerializer()

#     class Meta:
#         model = Registration
#         fields = '__all__'


# class ParticipantSerializer(serializers.ModelSerializer):
#     tournament = TournamentSerializer()
#     player = PlayerSerializer()

#     class Meta:
#         model = Participant
#         fields = '__all__'

# class MatchSerializer(serializers.ModelSerializer):
#     team_1 = OrganizationSerializer()
#     team_2 = OrganizationSerializer()
#     tournament = TournamentSerializer()

#     class Meta:
#         model = Match
#         fields = '__all__'


# class TournamentBracketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TournamentBracket
#         fields = '__all__'


# class LivePageSerializer(serializers.ModelSerializer):
#     tournament = TournamentSerializer()

#     class Meta:
#         model = LivePage
#         fields = '__all__'

# class AnnouncementSerializer(serializers.ModelSerializer):
#     tournament = TournamentSerializer()

#     class Meta:
#         model = Announcement
#         fields = '__all__'

# class BannerImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BannerImage
#         fields = '__all__'

# class PrizePoolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrizePool
#         fields = '__all__'

# class ResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Result
#         fields = '__all__'

from rest_framework import serializers
from .models import *
from account.serializers import UserProfileSerializer,OrganizationSerializer,OrganizerSerializer

class EliminationModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EliminationMode
        fields = ('id', 'elimination_mode')

class GameSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_name','game_type')

class GameSerializer(serializers.ModelSerializer):
    elimination_modes = EliminationModeSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'game_name', 'game_image', 'game_type', 'elimination_modes')

class TeamOrgSerializer(serializers.ModelSerializer):
    players = UserProfileSerializer(many=True)
    manager = UserProfileSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'team_name','organization','team_image', 'game', 'team_type', 'players', 'manager','is_active')

class TeamSerializer(serializers.ModelSerializer):
    players = UserProfileSerializer(many=True)
    manager = UserProfileSerializer(read_only=True)
    game = GameSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'team_name','team_image', 'game', 'team_type', 'players', 'manager','is_active')

class TeamRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'team_name','team_image', 'team_type','is_active')

class EventSmallSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name', 'event_start_date', 'event_end_date','event_thumbnail','event_thumbnail_alt_description','slug','is_published')

class EventVerifySerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name','slug','is_verified')


class TournamentSmallesttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["slug","id","tournament_name"]

class EventDashSerializer(serializers.ModelSerializer):
    tournaments = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ('id', 'event_name','slug','tournaments')
    
    def get_tournaments(self, obj):
        tournaments = Tournament.objects.filter(event=obj)
        serializer = TournamentSmallesttSerializer(tournaments, many=True)
        return serializer.data

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name', 'event_description', 'event_start_date', 'event_end_date','event_thumbnail','event_thumbnail_alt_description','slug','is_published')

class EventFAQSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = EventFAQ
        fields = ('id', 'value', 'heading', 'detail','event')

class EventNewsFeedSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = EventNewsFeed
        fields = ('id', 'content', 'user','event')

class EventSponsorSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = EventSponsor
        fields = ('id', 'sponsor_name', 'sponsorship_category', 'sponsor_banner','order','event','sponsor_link')


class TournamentFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentFAQ
        fields = ('id', 'value', 'heading', 'detail')


class TournamentStreamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStreams
        fields = ('id', 'stream_title', 'url')

class TournamentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentSponsor
        fields = ('id', 'sponsor_name', 'sponsorship_category','order', 'sponsor_banner','sponsor_link')

class TournamentSmallSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = Tournament
        exclude = ['event']

class TournamentSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    faqs = TournamentFAQSerializer(many=True, read_only=True)
    sponsors = TournamentSponsorSerializer(many=True, read_only=True)
    streams = TournamentStreamsSerializer(many=True, read_only=True)
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Tournament
        exclude = ['event']

class TournamentSmallestSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    class Meta:
        model = Tournament
        fields = "__all__"


class TournamentVerifySerializer(serializers.ModelSerializer):
    event = EventVerifySerializer(read_only=True)
    organizer = OrganizerSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    class Meta:
        model = Tournament
        fields = ['id','slug','is_verified','tournament_mode','is_published','tournament_name','event','organizer','game']


class StageSerializer(serializers.ModelSerializer):
    stage_elimation_mode = EliminationModeSerializer(read_only=True)
    tournament = TournamentSerializer(read_only=True)

    class Meta:
        model = Stage
        fields = ['id', 'stage_elimation_mode', 'stage_number',  'input_no_of_teams','output_no_of_teams', 'stage_name', 'tournament']


class SoloTournamentRegistrationSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = SoloTournamentRegistration
        fields = ['id','player','registration_status']


class TeamTournamentRegistrationSerializer(serializers.ModelSerializer):
    team = TeamRegisterSerializer(read_only=True)
    class Meta:
        model = TeamTournamentRegistration
        fields = "__all__"



class SoloMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloMatch
        fields = '__all__'

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'

class SingleEliminationRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleEliminationRound
        fields = "__all__"

class SingleEliminationMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleEliminationMatches
        fields = "__all__"

class DoubleEliminationRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleEliminationRound
        fields = "__all__"

class DoubleEliminationMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleEliminationMatches
        fields = "__all__"

class TournamentPrizePoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentPrizePool
        fields = "__all__"

class BattleRoyaleMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRoyalMatch
        fields = "__all__"

class BattleRoyalTeamDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRoyalTeamDetails
        fields = "__all__"

class BattleRoyalPlayerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleRoyalPlayerDetails
        fields = "__all__"
from rest_framework import serializers
from .models import (EliminationMode, EventNewsFeed, Game, Team, Event, EventFAQ, EventSponsor,
                     Tournament, TournamentFAQ, TournamentSponsor, TournamentStreams, Stage,SoloTournamentRegistration,TeamTournamentRegistration,SoloGroup,TeamGroup,SoloMatch,TeamMatch)
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

class EventSmallSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name', 'event_start_date', 'event_end_date','event_thumbnail','event_thumbnail_alt_description','slug')

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name', 'event_description', 'event_start_date', 'event_end_date','event_thumbnail','event_thumbnail_alt_description','slug')

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

class TournamentSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    faqs = TournamentFAQSerializer(many=True, read_only=True)
    sponsors = TournamentSponsorSerializer(many=True, read_only=True)
    streams = TournamentStreamsSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        exclude = ['event']


class StageSerializer(serializers.ModelSerializer):
    stage_elimation_mode = EliminationModeSerializer(read_only=True)
    tournament = TournamentSerializer(read_only=True)

    class Meta:
        model = Stage
        fields = ('id', 'stage_elimation_mode', 'stage_number', 'no_of_participants', 'no_of_groups', 'stage_name', 'tournament')


class SoloTournamentRegistrationSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    players = UserProfileSerializer(read_only=True)

    class Meta:
        model = SoloTournamentRegistration
        fields = '__all__'


class TeamTournamentRegistrationSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)
    players = UserProfileSerializer(read_only=True)
    team = TeamOrgSerializer(read_only=True)
    class Meta:
        model = TeamTournamentRegistration
        fields = '__all__'


class SoloGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloGroup
        fields = '__all__'
        
class TeamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamGroup
        fields = '__all__'


class SoloMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloMatch
        fields = '__all__'

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'

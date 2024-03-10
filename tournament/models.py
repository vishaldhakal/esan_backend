from django.db import models
from ckeditor.fields import RichTextField
from account.models import Player, UserProfile,Organizer,Organization
from django.db.models.signals import post_save
from django.dispatch import receiver

class EliminationMode(models.Model):
    STAGE_ELIMINTAION_MODES = (
        ('Single Elimination','Single Elimination'),
        ('Double Elimination','Double Elimination'),
        ('Battle Royale','Battle Royale'),
        ('Round Robin','Round Robin'),
    )
    elimination_mode = models.CharField(max_length=500,choices=STAGE_ELIMINTAION_MODES)

    def __str__(self) -> str:
        return self.elimination_mode
class Game(models.Model):  
    GAME_TYPE_CHOICES = (
        ('PC','PC'),
        ('Mobile','Mobile'),
    )
    game_name = models.CharField(max_length=500)
    game_image = models.FileField()
    game_type = models.CharField(max_length=100,choices=GAME_TYPE_CHOICES,default='Mobile')
    elimination_modes = models.ManyToManyField(EliminationMode)

    def __str__(self) -> str:
        return self.game_name +" " +self.game_type

class Team(models.Model):
    TEAM_TYPE_CHOICES = (
        ('Duo','Duo'),
        ('Squad','Squad'),
    )
    team_name = models.CharField(max_length=500)
    team_image = models.FileField()
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    team_type = models.CharField(max_length=500,choices=TEAM_TYPE_CHOICES,default="Squad")
    players = models.ManyToManyField(UserProfile,blank=True,related_name='players')
    manager = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,related_name='manager')
    organization = models.ForeignKey(Organization,on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.team_name

class Event(models.Model):
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=700)
    event_name = models.CharField(max_length=700,unique=True)
    event_thumbnail = models.FileField(blank=True)
    event_thumbnail_alt_description = models.CharField(max_length=500,blank=True)
    event_description = RichTextField(blank=True)
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.event_name
    
class EventFAQ(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    heading = models.CharField(max_length=1000)
    detail = models.TextField()

    def __str__(self) -> str:
        return self.heading

class EventNewsFeed(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    content = RichTextField()
    user = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class EventSponsor(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    sponsor_name = models.CharField(max_length=500)
    sponsorship_category = models.CharField(max_length=500)
    sponsor_banner = models.FileField()
    order = models.IntegerField(default=0)
    sponsor_link = models.CharField(max_length=500,blank=True)

    def __str__(self) -> str:
        return self.sponsor_name

class Tournament(models.Model):
    TOURNAMENT_MODE_CHOICES = (
        ('Online','Online'),
        ('LAN','LAN'),
    )

    TOURNAMENT_PARTICIPANTS = (
        ('Player','Player'),
        ('Team','Team'),
    )

    TOURNAMENT_STATUS = (
        ('Live', 'Live'),
        ('Past', 'Past'),
        ('Upcoming', 'Upcoming')
    )
    slug = models.SlugField(max_length=100 ,unique=True)
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE,related_name='organizer')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event')
    location = models.CharField(max_length=100,blank=True)
    tournament_name = models.CharField(max_length=700)
    tournament_logo = models.FileField(blank=True)
    tournament_banner = models.FileField(blank=True)
    tournament_mode = models.CharField(max_length=700,choices=TOURNAMENT_MODE_CHOICES,default='Online')
    tournament_status = models.CharField(max_length=50, choices=TOURNAMENT_STATUS,default="Upcoming")
    tournament_participants = models.CharField(max_length=700,choices=TOURNAMENT_PARTICIPANTS,default='Team')
    is_free = models.BooleanField(default=False)
    tournament_fee = models.FloatField(blank=True,null=True)
    maximum_no_of_participants = models.IntegerField(default=0)
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='game')
    tournament_description = RichTextField(blank=True)
    tournament_short_description = models.CharField(blank=True, max_length= 150)
    tournament_rules = RichTextField(blank=True)
    tournament_prize_pool = RichTextField(blank=True)
    registration_opening_date = models.DateTimeField(blank=True,null=True)
    registration_closing_date = models.DateTimeField(blank=True,null=True)
    tournament_start_date = models.DateTimeField(blank=True,null=True)
    tournament_end_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_registration_enabled = models.BooleanField(default=False)
    accept_registration_automatic = models.BooleanField(default=False)
    contact_email = models.CharField(max_length=500,blank=True)
    discord_link = models.URLField(max_length=500,blank=True)
    is_verified = models.BooleanField(default=False)
    no_of_participants = models.IntegerField(default=0)
    live_link = models.TextField(blank=True,null=True)

    def update_no_of_participants_by_team(self):
        self.no_of_participants = self.team_registrations.count()
        self.save()

    def update_no_of_participants_by_solo(self):
            self.no_of_participants = self.solo_registrations.count()
            self.save()

    def __str__(self) -> str:
        return self.tournament_name


class SoloTournamentRegistration(models.Model):
    REGISTRATION_STATUS_CHOICES = (
        ('Ongoing Review','Ongoing Review'),
        ('Verified','Verified'),
        ('Rejected','Rejected'),
    )
    
    PAYMENT_CHOICES = (
        ('Cash','Cash'),
        ('Bank Transfer','Bank Transfer'),
        ('Esewa','Esewa'),
        ('Other','Other'),
    )

    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE, related_name='solo_registrations')
    player = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    registration_fee = models.FloatField()
    registration_status = models.CharField(max_length=500, choices=REGISTRATION_STATUS_CHOICES, default="Ongoing Review")
    payment_method = models.CharField(max_length=500, choices=PAYMENT_CHOICES, default="Other")

    def __str__(self) -> str:
        return self.player.username
@receiver(post_save, sender=SoloTournamentRegistration)
def update_tournament_no_of_participants(sender, instance, created, **kwargs):
    tournament = instance.tournament
    tournament.update_no_of_participants_by_solo()

class TeamTournamentRegistration(models.Model):
    REGISTRATION_STATUS_CHOICES = (
        ('Ongoing Review','Ongoing Review'),
        ('Verified','Verified'),
        ('Rejected','Rejected'),
    )
    
    PAYMENT_CHOICES = (
        ('Cash','Cash'),
        ('Bank Transfer','Bank Transfer'),
        ('Esewa','Esewa'),
        ('Khalti','Khalti'),
        ('Other','Other'),
    )

    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='team_registrations')
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    registration_status = models.CharField(max_length=500,choices=REGISTRATION_STATUS_CHOICES,default="Ongoing Review")
    payment_method = models.CharField(max_length=500,choices=PAYMENT_CHOICES,default="Other")

    def __str__(self) -> str:
        return self.team.team_name

@receiver(post_save, sender=TeamTournamentRegistration)
def update_tournament_no_of_participants(sender, instance, created, **kwargs):
    tournament = instance.tournament
    tournament.update_no_of_participants_by_team()
    
class TournamentStreams(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='streams')
    stream_title = models.CharField(max_length=500)
    url = models.URLField(max_length=500)

    def __str__(self) -> str:
        return self.stream_name
    
class TournamentSponsor(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='sponsors')
    sponsor_name = models.CharField(max_length=500)
    sponsor_link = models.CharField(max_length=500,blank=True)
    sponsorship_category = models.CharField(max_length=500)
    sponsor_banner = models.FileField()
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.sponsor_name
    
class TournamentPrizePool(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='tournament_prize_pools')
    placement = models.CharField(max_length=500,blank=True,null=True)
    prize = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.placement

class TournamentFAQ(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='faqs')
    value = models.CharField(max_length=100)
    heading = models.CharField(max_length=1000)
    detail = models.TextField()

    def __str__(self) -> str:
        return self.heading
    
class Stage(models.Model):
    stage_number = models.IntegerField()
    stage_name = models.CharField(max_length=500)
    stage_elimation_mode = models.ForeignKey(EliminationMode,on_delete=models.DO_NOTHING)
    input_no_of_teams = models.IntegerField()
    output_no_of_teams = models.IntegerField()
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.stage_name
    
class SingleEliminationRound(models.Model):
    round_name = models.CharField(max_length=500, blank=True, null=True,)
    start_date_time = models.DateTimeField(blank=True, null=True,)
    number_of_matches = models.IntegerField(blank=True, null=True,)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True,)

class SingleEliminationMatches(models.Model):
    match_name = models.CharField(max_length=500, blank=True, null=True)
    round = models.ForeignKey(SingleEliminationRound, on_delete=models.CASCADE, default=1)
    team1 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="SingleEliminationTeam1", blank=True, null=True,)
    team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="SingleEliminationTeam2", blank=True, null=True,)
    player1 = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="SingleEliminationPlayer1", blank=True, null=True,)
    player2 = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="SingleEliminationPlayer2", blank=True, null=True,)
    winner = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="winner", blank=True, null=True,)
    pWinner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="player_winner", blank=True, null=True,)
    start_date_time = models.DateTimeField(blank=True, null=True)

class DoubleEliminationRound(models.Model):
    RESULT_CHOICES = (
        ('WB','WB'),
        ('LB','LB'),
    )
    round_name = models.CharField(max_length=500, blank=True, null=True,)
    bracket = models.CharField(max_length=500,choices=RESULT_CHOICES,default='WB')
    start_date_time = models.DateTimeField(blank=True, null=True,)
    number_of_matches = models.IntegerField(blank=True, null=True,)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True,)

class DoubleEliminationMatches(models.Model):
    match_name = models.CharField(max_length=500,blank=True, null=True,)
    round = models.ForeignKey(DoubleEliminationRound, on_delete=models.CASCADE, default=1)
    team1 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="DoubleEliminationTeam1", blank=True, null=True,)
    team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="DoubleEliminationTeam2", blank=True, null=True,)
    player1 = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="DoubleEliminationPlayer1", blank=True, null=True,)
    player2 = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="DoubleEliminationPlayer2", blank=True, null=True,)
    pWinner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="DoubleEliminationPlayerWinner", blank=True, null=True,)
    winner = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="DoubleEliminationMatchWinner", blank=True, null=True,)
    start_date_time = models.DateTimeField(blank=True, null=True)
    
    
class SoloMatch(models.Model):
    RESULT_CHOICES = (
        ('WIN','WIN'),
        ('LOSE','LOSE'),
        ('DRAW','DRAW'),
    )
    stage = models.ForeignKey(Stage,on_delete=models.DO_NOTHING)
    player1 = models.ForeignKey(UserProfile,related_name='player1',on_delete=models.DO_NOTHING)
    player2 = models.ForeignKey(UserProfile,related_name='player2',on_delete=models.DO_NOTHING)
    player1_points = models.FloatField()
    player2_points = models.FloatField()
    player1_result = models.CharField(max_length=500,choices=RESULT_CHOICES)
    player2_result = models.CharField(max_length=500,choices=RESULT_CHOICES)

    def __str__(self) -> str:
        return self.player1.username + " VS " + self.player2.username

class TeamMatch(models.Model):
    RESULT_CHOICES = (
        ('WIN','WIN'),
        ('LOSE','LOSE'),
        ('DRAW','DRAW'),
        ('ABORTED','ABORTED'),
        ('ABORTED','ABORTED'),
    )
    stage = models.ForeignKey(Stage,on_delete=models.DO_NOTHING)
    team1 = models.ForeignKey(Team,related_name='team1',on_delete=models.DO_NOTHING)
    team2 = models.ForeignKey(Team,related_name='team2',on_delete=models.DO_NOTHING)
    team1_points = models.FloatField()
    team2_points = models.FloatField()
    team1_result = models.CharField(max_length=500,choices=RESULT_CHOICES)
    team2_result = models.CharField(max_length=500,choices=RESULT_CHOICES)

    def __str__(self) -> str:
        return self.team1.team_name + " VS " + self.team2.team_name

class BattleRoyalMatch(models.Model):
    stage = models.ForeignKey(Stage,  on_delete=models.CASCADE, related_name="battle_royale_stage", blank=True, null=True,)
    start_date_time = models.DateTimeField(blank=True, null=True)

class BattleRoyalPlayerDetails(models.Model):
    battleRoyale = models.ForeignKey(BattleRoyalMatch, on_delete=models.CASCADE, related_name="battle_royale_player", blank=True, null=True,)
    players = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name="BattleRoyalePlayer", blank=True)
    placement = models.IntegerField(blank=True, null=True)
    killPoints = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)

class BattleRoyalTeamDetails(models.Model):
    battleRoyale = models.ForeignKey(BattleRoyalMatch, on_delete=models.CASCADE, related_name="battle_royale_team", blank=True, null=True,)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="BattleRoyaleTeam", blank=True)
    placement = models.IntegerField(blank=True, null=True)
    killPoints = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
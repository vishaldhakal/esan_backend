from django.db import models
from ckeditor.fields import RichTextField
from account.models import Player, UserProfile,Organizer,Organization
    
class EliminationMode(models.Model):
    STAGE_ELIMINTAION_MODES = (
        ('Single Elimination','Single Elimination'),
        ('Double Elimination','Double Elimination'),
        ('Battle Royale','Battle Royale'),
        ('Round Robbin','Round Robbin'),
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
    organizer = models.ForeignKey(Organizer,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
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
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
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

    def __str__(self) -> str:
        return self.tournament_name
    
    

    
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

class TournamentFAQ(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='faqs')
    value = models.CharField(max_length=100)
    heading = models.CharField(max_length=1000)
    detail = models.TextField()

    def __str__(self) -> str:
        return self.heading
    
class Stage(models.Model):
    stage_elimation_mode = models.ForeignKey(EliminationMode,on_delete=models.DO_NOTHING)
    stage_number = models.IntegerField()
    no_of_participants = models.IntegerField()
    no_of_groups = models.IntegerField()
    stage_name = models.CharField(max_length=500)
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.stage_name
    
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

    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)
    player = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    registration_fee = models.FloatField()
    registration_status = models.CharField(max_length=500,choices=REGISTRATION_STATUS_CHOICES,default="Ongoing Review")
    payment_method = models.CharField(max_length=500,choices=PAYMENT_CHOICES,default="Other")
    current_stage = models.ForeignKey(Stage,related_name="current_stage",null=True,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.player.username

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
        ('Other','Other'),
    )

    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    registration_fee = models.FloatField()
    registration_status = models.CharField(max_length=500,choices=REGISTRATION_STATUS_CHOICES,default="Ongoing Review")
    payment_method = models.CharField(max_length=500,choices=PAYMENT_CHOICES,default="Other")
    current_stage = models.ForeignKey(Stage,related_name="current_stagee",null=True,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.team.team_name

class SoloGroup(models.Model):
    group_name = models.CharField(max_length=500)
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE)
    participants = models.ManyToManyField(UserProfile)

    def __str__(self) -> str:
        return self.group_name

class TeamGroup(models.Model):
    group_name = models.CharField(max_length=500)
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE)
    participants = models.ManyToManyField(Team)

    def __str__(self) -> str:
        return self.group_name
    
class SoloMatch(models.Model):
    RESULT_CHOICES = (
        ('WIN','WIN'),
        ('LOSE','LOSE'),
        ('DRAW','DRAW'),
    )
    stage = models.ForeignKey(Stage,on_delete=models.DO_NOTHING)
    group = models.ForeignKey(SoloGroup,on_delete=models.DO_NOTHING)
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
    )
    stage = models.ForeignKey(Stage,on_delete=models.DO_NOTHING)
    group = models.ForeignKey(TeamGroup,on_delete=models.DO_NOTHING)
    team1 = models.ForeignKey(Team,related_name='team1',on_delete=models.DO_NOTHING)
    team2 = models.ForeignKey(Team,related_name='team2',on_delete=models.DO_NOTHING)
    team1_points = models.FloatField()
    team2_points = models.FloatField()
    team1_result = models.CharField(max_length=500,choices=RESULT_CHOICES)
    team2_result = models.CharField(max_length=500,choices=RESULT_CHOICES)

    def __str__(self) -> str:
        return self.team1.team_name + " VS " + self.team2.team_name

    
class TournamentBracket(models.Model):
    bracket_types = (
        ('Winner Bracket', 'Winner Bracket'),
        ('Looser Bracket', 'Looser Bracket')
    )
    bracket_type = models.CharField(choices=bracket_types, max_length=30)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Team, related_name='Team_participants')
    def __str__(self):
        return f'{self.bracket_type} for {self.tournament}'

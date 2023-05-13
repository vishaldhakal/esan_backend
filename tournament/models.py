from django.db import models
from ckeditor.fields import RichTextField
from account.models import  Organization, Organizer, Player

class Team(models.Model):
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    captain = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='captain_of')
    members = models.ManyToManyField(Player, related_name='member_of', blank=True)
    team_manager = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='manager_of')

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-start_date',)

class Tournament(models.Model):
    PARTICIPANT_TYPE_CHOICES = [
        ('Solo', 'Solo'),
        ('Duo', 'Duo'),
        ('Squad', 'Squad')
    ]
    TOURNAMENT_TYPE_CHOICES = [
        ('Single Elimination', 'Single Elimination'),
        ('Double Elimination', 'Double Elimination'),
        ('League', 'League'),
        ('Battle Royal', 'Battle Royal')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = RichTextField()
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2)
    participant_type = models.CharField(choices=PARTICIPANT_TYPE_CHOICES, max_length=10)
    tournament_type = models.CharField(max_length=20, choices=TOURNAMENT_TYPE_CHOICES)
    number_of_participants = models.PositiveBigIntegerField()
    def __str__(self):
        return self.name

class BannerImage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tournament_banners/')

    def __str__(self):
        return f"{self.tournament.name} Banner"
    
class PrizePool(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.TextField(max_length=20)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    extras = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.tournament.name} - {self.extras}: {self.amount}"


class Registration(models.Model):
    PAYMENT_CHOICES = [
        ('Esewa','Esewa'),
        ('Khalti', 'Khalti'),
        ('Card', 'Card')
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(choices= PAYMENT_CHOICES, max_length=20)
    amount = models.FloatField()
    date_registered = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=400, blank=True)
    def __str__(self):
            return f"{self.team} registered for {self.tournament}"

class Game(models.Model):
    GAME_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Physical', 'Physical'),
    ]
    GAME_PLATFORM = [
        ('Mobile', 'Mobile'),
        ('Console', 'Console'),
        ('PC', 'PC')
    ]
    game_platform = models.CharField(max_length=15, choices=GAME_PLATFORM)
    name = models.CharField(max_length=300)
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    description = RichTextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

   
class TournamentBracket(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='brackets')
    number_of_rounds = models.PositiveSmallIntegerField()
    rounds_per_match = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='won_brackets')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='lost_brackets')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    number_of_teams = models.PositiveSmallIntegerField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['number_of_rounds']

    def __str__(self):
        return f'Bracket for {self.tournament}'
    
class Round(models.Model):
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bracket.tournament.name} - Round {self.round_number}"   

class Group(models.Model):
    Elimination_mode = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('None', 'None')
    ]
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    elimination_mode = models.CharField(max_length=20, choices=Elimination_mode)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tournament.name} - {self.name}"
    
class Stage(models.Model):
    Status=[
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing')
    ]
    name = models.CharField(max_length=50)
    groups = models.ManyToManyField(Group, related_name='groups')
    status = models.CharField(max_length= 20, choices=Status)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

class Match(models.Model):
    MATCH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    match_number = models.IntegerField()
    number_of_rounds = models.PositiveBigIntegerField()
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_2')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.team_1.name} vs {self.team_2.name} in {self.game.name} - {self.status}"

class Schedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    venue = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tournament.name} - {self.match.match_number} - {self.start_time} - {self.end_time}"
    
class Result(models.Model):
    RESULT_CHOICES = [
        ('Team_1', 'Team 1 wins'),
        ('Team_2', 'Team 2 wins'),
        ('Draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="results")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_result")

    def __str__(self):
        return f"{self.tournament} - {self.match.match_number} - {self.result}"

class Sponsor(models.Model):
    SPONSOR_TYPE_CHOICES = [
        ('title', 'Title Sponsor'),
        ('presenting', 'Presenting Sponsor'),
        ('official', 'Official Sponsor'),
        ('media', 'Media Partner'),
        ('support', 'Support Sponsor'),
        ('technical', 'Technical Sponsor'),
        ('gaming', 'Gaming Partner'),
        ('food_and_beverages', 'Food and Beverages Sponsor'),
        ('venue', 'Venue Sponsor'),
        ('merchandise', 'Merchandise Partner'),
        ('broadcast', 'Broadcast Partner'),
    ]
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/', null=True)
    type = models.CharField(max_length=40, choices=SPONSOR_TYPE_CHOICES)
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE, related_name='sponsor')
    def __str__(self):
        return f"{self.name} - {self.type} for {self.tournament.name}"
    

class LivePage(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True)
    chat_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.tournament.name

class Announcement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.event.name} - {self.title}'




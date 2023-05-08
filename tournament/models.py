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
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
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
        ('Single', 'Single'),
        ('Double', 'Double'),
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


class SoloRegistration(models.Model):
    PAYMENT_CHOICES = [
        ('esewa','esewa'),
        ('Khalti', 'Khalti'),
        ('Card', 'Card')
    ]
    Status = [
        ('Eliminated', 'Eliminated'),
        ('Playing', 'Playing')
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(choices= PAYMENT_CHOICES, max_length=20)
    amount = models.FloatField()
    remarks = models.CharField(max_length=400)
    status = models.CharField(max_length=20, choices=Status)
    points = models.PositiveBigIntegerField()
    ranking = models.PositiveBigIntegerField()


    def __str__(self):
            return f"{self.player} registered for {self.tournament}"
class DuoRegistration(models.Model):
    PAYMENT_CHOICES = [
        ('esewa','esewa'),
        ('Khalti', 'Khalti'),
        ('Card', 'Card')
    ]
    Status = [
        ('Eliminated', 'Eliminated'),
        ('Playing', 'Playing')
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(choices= PAYMENT_CHOICES, max_length=20)
    amount = models.FloatField()
    remarks = models.CharField(max_length=400)
    status = models.CharField(max_length=20, choices=Status)
    points = models.PositiveBigIntegerField()
    ranking = models.PositiveBigIntegerField()

    def __str__(self):
            return f"{self.team} registered for {self.tournament}"
class SquadRegistration(models.Model):
    PAYMENT_CHOICES = [
        ('esewa','esewa'),
        ('Khalti', 'Khalti'),
        ('Card', 'Card')
    ]
    Status = [
        ('Eliminated', 'Eliminated'),
        ('Playing', 'Playing')
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(choices= PAYMENT_CHOICES, max_length=20)
    amount = models.FloatField()
    remarks = models.CharField(max_length=400)
    status = models.CharField(max_length=20, choices=Status)
    points = models.PositiveBigIntegerField()
    ranking = models.PositiveBigIntegerField()
    def __str__(self):
            return f"{self.team} registered for {self.tournament}"
        

# class Registration(models.Model):
#     team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
#     team_logo = models.ImageField(upload_to='team_logos/')
#     captain = models.ManyToManyField(Player, related_name='captain')
#     players = models.ManyToManyField(Player, related_name='registrations', blank=True)
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return self.team_name

class Game(models.Model):
    
    GAME_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Physical', 'Physical'),
    ]
    GAME_PLATFORM = [
        ('mobile', 'Mobile'),
        ('console', 'Console'),
        ('pc', 'PC')
    ]
    game_platform = models.CharField(max_length=15, choices=GAME_PLATFORM)
    name = models.CharField(max_length=300)
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    description = RichTextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.game_type} - {self.tournament.name}"

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ManyToManyField(Player, related_name='participated_players')
    team = models.ManyToManyField(Team, related_name='participated_teams')

   
class TournamentBracket(models.Model):
    TOURNAMENT_TYPE_CHOICES = [
        ('single_elimination', 'Single Elimination'),
        ('double_elimination', 'Double Elimination'),
        ('round_robin', 'Round Robin'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='brackets')
    type = models.CharField(max_length=50, choices=TOURNAMENT_TYPE_CHOICES)
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
        return f'{self.type} Bracket for {self.tournament}'
    
class Round(models.Model):
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bracket.tournament.name} - Round {self.round_number}"   

class SoloGroup(models.Model):
    Elimination_mode = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('None', 'None')
    ]
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    elimination_mode = models.CharField(max_length=20, choices=Elimination_mode)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    group_number = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} - {self.name}"
    
class DuoGroup(models.Model):
    Elimination_mode = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('None', 'None')
    ]
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    elimination_mode = models.CharField(max_length=20, choices=Elimination_mode)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    group_number = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} - {self.name}"
class SquadGroup(models.Model):
    Elimination_mode = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('None', 'None')
    ]
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    elimination_mode = models.CharField(max_length=20, choices=Elimination_mode)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    group_number = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} - {self.name}"

class SoloStage(models.Model):
    Status=[
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing')
    ]
    name = models.CharField(max_length=50)
    groups = models.ManyToManyField(SoloGroup, related_name='solo_groups')
    status = models.CharField(max_length= 20, choices=Status)
class DuoStage(models.Model):
    Status=[
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing')
    ]
    name = models.CharField(max_length=50)
    groups = models.ManyToManyField(DuoGroup, related_name='solo_groups')
    status = models.CharField(max_length= 20, choices=Status)
class SquadStage(models.Model):
    Status=[
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing')
    ]
    name = models.CharField(max_length=50)
    groups = models.ManyToManyField(SquadGroup, related_name='solo_groups')
    status = models.CharField(max_length= 20, choices=Status)

class SoloMatch(models.Model):
    MATCH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    number_of_rounds = models.PositiveBigIntegerField()
    match_number = models.IntegerField()
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_player_1')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_player_2')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.player_1.user.username} vs {self.player_2.user.username} - {self.tournament.name}"

class DuoMatch(models.Model):
    MATCH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    number_of_rounds = models.PositiveBigIntegerField()
    match_number = models.IntegerField()
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_2')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.team_1.name} vs {self.team_2.name} - {self.tournament.name}"

class SquadMatch(models.Model):
    MATCH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    number_of_rounds = models.PositiveBigIntegerField()
    match_number = models.IntegerField()
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='squad_match_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='squad_match_team_2')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.team_1.user.username} vs {self.team_2.user.username} - {self.tournament.name}"


class SoloSchedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(SoloMatch, on_delete=models.CASCADE, related_name='solo_match_schedule')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class DuoSchedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(DuoMatch, on_delete=models.CASCADE, related_name='duo_match_schedule')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class SquadSchedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(SquadMatch, on_delete=models.CASCADE, related_name='squad_match_schedule')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
class SoloResult(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(SoloMatch, on_delete=models.CASCADE, related_name="solo_match_result")
    created_at = models.DateTimeField(auto_now_add=True)
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    player_1 = models.PositiveIntegerField()
    player_2 = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.tournament} - {self.result}"
    
class DuoResult(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(DuoMatch, on_delete=models.CASCADE, related_name="duo_match_result")
    created_at = models.DateTimeField(auto_now_add=True)
    RESULT_CHOICES = [
        ('team_1', 'Team 1 wins'),
        ('team_2', 'Team 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    team_1 = models.PositiveIntegerField()
    team_2 = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.tournament} - {self.result}"
    
class SquadResult(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match = models.ForeignKey(SquadMatch, on_delete=models.CASCADE, related_name="squad_match_result")
    created_at = models.DateTimeField(auto_now_add=True)
    RESULT_CHOICES = [
        ('team_1', 'Team 1 wins'),
        ('team_2', 'Team 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    team_1 = models.PositiveIntegerField()
    team_2 = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.tournament} - {self.result}"

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
        return self.name
    

class LivePage(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True)
    chat_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.tournament.name

class Announcement(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)




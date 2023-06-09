from django.contrib import admin
from .models import EliminationMode,Tournament,Team,Game,Event,SoloTournamentRegistration,TeamTournamentRegistration,TournamentSponsor,EventSponsor,Stage,SoloMatch,TeamMatch,TournamentFAQ,EventFAQ

admin.site.register(Tournament)
admin.site.register(EliminationMode)
admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(SoloTournamentRegistration)
admin.site.register(TeamTournamentRegistration)
admin.site.register(TournamentSponsor)
admin.site.register(EventSponsor)
admin.site.register(TournamentFAQ)
admin.site.register(EventFAQ)
admin.site.register(Stage)
admin.site.register(SoloMatch)
admin.site.register(TeamMatch)

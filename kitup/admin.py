from django.contrib import admin

# Import the models that are being registered.
from kitup.models import Profile, Sport, Match, MatchParticipant, PlayerReport

# Registration of the models.
admin.site.register(Profile)
admin.site.register(Sport)
admin.site.register(Match)
admin.site.register(MatchParticipant)
admin.site.register(PlayerReport)

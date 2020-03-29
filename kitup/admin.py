from django.contrib import admin
from kitup.models import Profile, Player, Match, Report, Sport

# Registration of the models.
admin.site.register(Profile)
admin.site.register(Sport)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Report)

from django.contrib import admin
from kitup.models import Users, Player, Match, Report, Sport

# Register your models here.

admin.site.register(Users)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Report)
admin.site.register(Sport)
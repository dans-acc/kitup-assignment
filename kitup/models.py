from django.db import models
from django.utils import timezone

# This is the users table
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    rating = models.IntegerField()
    strikes = models.IntegerField()
    joined_on = models.DateTimeField(default=timezone.now())
    last_login = models.DateTimeField()
    age = models.IntegerField()

    def __str__(self):
        return self.forename + " " + self.surname

class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    team_size = models.IntegerField()

    def __str__(self):
        return self.name

# This is the match table
class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField()
    min_rating = models.IntegerField()
    team_home_score = models.IntegerField()
    team_away_score = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()


# This is the match player table
class Player(models.Model):
    player_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.IntegerField()

    class Meta:
        unique_together = ('player_id', 'game_id')


# This is the report a player table
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_maker = models.IntegerField()
    report_subject = models.IntegerField()
    reason = models.CharField(max_length=20)

    def __str__(self):
        return self.report_id
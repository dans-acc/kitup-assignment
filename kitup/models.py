from django.db import models
from django.contrib.auth.models import User


# Profile defines the individual users registered for the site.
# Model extends the default User model implemented by django.
class Profile(models.Model):

    # Create a one-to-one-link between the profile and the user.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional user information.
    profile_picture = models.ImageField(upload_to='profile_images')
    age = models.IntegerField()

    # Game specific information.
    rating = models.IntegerField(default=0)
    strikes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Profiles'

    # Make use of the user models username.
    def __str__(self):
        return self.user.username

# Defines the sport table i.e. the game type.
class Sport(models.Model):

    NAME_MAX_LENGTH = 30

    # The name of the sport and the maximum team sizes.
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    max_team_size = models.IntegerField()

    # Returns a user friendly name for the sport.
    def __str__(self):
        return self.name

# Defines the match table; contains information pertaining to created matches.
class Match(models.Model):

    NAME_MAX_LENGTH = 30

    DEFAULT_MIN_AGE = 16
    DEFAULT_MAX_AGE = 68
    DEFAULT_MIN_RATING = 0

    # Attributes pertaining to the match type.
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    match_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    start_datetime = models.DateTimeField(null=True)
    duration = models.IntegerField()

    # Age restructions for the match.
    min_age = models.IntegerField(default=DEFAULT_MIN_AGE)
    max_age = models.IntegerField(default=DEFAULT_MAX_AGE)

    # Rating restrictions for the match.
    min_rating = models.IntegerField(default=DEFAULT_MIN_RATING)

    # Post match team values.
    team_home_score = models.IntegerField(default=0)
    team_away_score = models.IntegerField(default=0)

    # Match customisation
    match_photo = models.ImageField(upload_to='match_images')

    class Meta:
        verbose_name_plural = 'Matches'

    # Returns the name of the match.
    def __str__(self):
        return self.name

# Defines a player within a match.
class Player(models.Model):

    # The user and the match for which this entry exists.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    # The team to which they belong.
    team = models.IntegerField()

    # Defines meta attributes pertaining to the Player model.
    class Meta:
        verbose_name_plural = 'Players'
        unique_together = ('user', 'match')

    # Defines the name of the model.
    def __str__(self):
        return user.username

# Defines the model used to report other users.
class Report(models.Model):

    REASON_MAX_LENGTH = 60

    # Defines the reporting and reported users.
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporting_user')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')

    # The reason for the report.
    reason = models.CharField(max_length = REASON_MAX_LENGTH)

    class Meta:
        verbose_name_plural = 'Reports'

    # A string representation of the report.
    def __str__(self):
        return self.report_id




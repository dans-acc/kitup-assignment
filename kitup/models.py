from django.db import models
from django.contrib.auth.models import User

# Profile defines the individual user's registered for the site.
# Fundamentally, the model extends the default User model implemented by django.
class Profile(models.Model):

    # Define constants for the user.
    USER_USERNAME_MIN_LENGTH = 8
    USER_USERNAME_MAX_LENGTH = 16

    # Define the profile constants.
    DEFAULT_RATING = 0

    # Additional user attributes.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images')
    date_of_birth = models.DateField(null=False)
    rating = models.IntegerField(default=DEFAULT_RATING)
    strikes = models.IntegerField(default=0)

    # Model meta data.
    class Meta:
        verbose_name_plural = 'Profiles'

    # Provide a user friendly name for the model.
    def __str__(self):
        return self.user.username

# Model defines the type of sport that can be played.
class Sport(models.Model):

    # Define sport model constants.
    NAME_MAX_LENGTH = 30

    # The name of the sport and individual team-sizes.
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    max_team_size = models.IntegerField()

    # Returns a user friendly name for the sport.
    def __str__(self):
        return self.name

# Model defines a match that has / is going to happened.
class Match(models.Model):

    # Defines the Match models constants.
    NAME_MAX_LENGTH = 30
    DEFAULT_MIN_AGE = 16
    DEFAULT_MAX_AGE = 68
    DEFAULT_MIN_RATING = 0

    # Attributes pertaining to the match type.
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=NAME_MAX_LENGTH, null=False)
    match_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)

    # Match times i.e. start date and time, and time it finishes.
    start_datetime = models.DateTimeField(null=False)
    end_time = models.TimeField(auto_now=False)

    # Restrictions on joining the match.
    min_age = models.IntegerField(default=DEFAULT_MIN_AGE)
    max_age = models.IntegerField(default=DEFAULT_MAX_AGE)
    min_rating = models.IntegerField(default=DEFAULT_MIN_RATING)

    # Post match team scores.
    team_home_score = models.IntegerField(default=0)
    team_away_score = models.IntegerField(default=0)

    # Model meta data.
    class Meta:
        verbose_name_plural = 'Matches'

    # Returns a user friendly name for the match.
    def __str__(self):
        return self.name

# Defines a player within a match.
class Player(models.Model):

    # The user and the match for which this entry exists.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.IntegerField()

    # Defines meta attributes pertaining to the Player model.
    class Meta:
        verbose_name_plural = 'Players'

    # Defines the name of the model.
    def __str__(self):
        return user.username 

# Defines the model used to report other users.
class Report(models.Model):

    # Defines report models constants.
    REASON_MAX_LENGTH = 60

    # The user making the report, the user in question, and the reason for the report, respectively.
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporting_user')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    reason = models.CharField(max_length = REASON_MAX_LENGTH)

    # Report models meta data.
    class Meta:
        verbose_name_plural = 'Reports'

    # A string representation of the report.
    def __str__(self):
        return self.report_id




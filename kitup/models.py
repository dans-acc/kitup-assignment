from django.db import models
from django.contrib.auth.models import User

from enum import Enum

# Profile defines the individual user's registered for the site.
# Fundamentally, the model extends the default User model implemented by django.
class Profile(models.Model):

    # User constants.
    USER_USERNAME_MIN_LEN = 8
    USER_USERNAME_MAX_LEN = 16

    # Restrictions.
    MIN_AGE = 14

    # Defaults.
    RATING_DEFAULT = 0

    # Additional user attributes.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images')
    date_of_birth = models.DateField(null=False)
    rating = models.FloatField(default=RATING_DEFAULT)
    reported = models.IntegerField(default=0)

    # Model meta data.
    class Meta:
        verbose_name_plural = 'Profiles'

    # Provide a user friendly name for the model.
    def __str__(self):
        return self.user.username


# Defines the sports types.
class Sport(models.Model):

    # Define sport model constants.
    NAME_MAX_LEN = 30

    # The name of the sport and individual team-sizes.
    name = models.CharField(max_length=NAME_MAX_LEN)
    max_participants = models.IntegerField()
    sport_picture = models.ImageField(upload_to='sport_images')

    # Model metadata.
    class Meta:
        verbose_name_plural = 'Sports'

    # Returns a user friendly name for the sport.
    def __str__(self):
        return self.name

# Defines the match location.
class MatchLocation(models.Model):

    # Restrictions.
    NAME_MAX_LEN = 30
    ADDRESS_MAX_LEN = 40
    POST_CODE_MAX_LEN = 8
    CITY_MAX_LEN = 30
    LAT_LNG_MAX_DIGITS = 9
    LAT_LNG_DECIMAL_PLACES = 6

    # Attributes defining the match location.
    name = models.CharField(max_length=NAME_MAX_LEN)
    address = models.CharField(max_length=ADDRESS_MAX_LEN)
    post_code = models.CharField(max_length=POST_CODE_MAX_LEN)
    city = models.CharField(max_length=CITY_MAX_LEN)
    latitude = models.DecimalField(max_digits=LAT_LNG_MAX_DIGITS, decimal_places=LAT_LNG_DECIMAL_PLACES)
    longitude = models.DecimalField(max_digits=LAT_LNG_MAX_DIGITS, decimal_places=LAT_LNG_DECIMAL_PLACES)

    # Defines the model metadata.
    class Meta:
        verbose_name_plural = 'Match Locations'

    # A user friendly name for the model.
    def __str__(self):
        return self.name


# Model defines a match that has / is going to happened.
class Match(models.Model):
    
    # Restrictions.
    NAME_MAX_LEN = 30

    # Defaults.
    MIN_AGE_DEFAULT = Profile.MIN_AGE
    MAX_AGE_DEFAULT = 70
    MIN_RATING_DEFAULT = 0
    PRIVATE_DEFAULT = False

    # Attributes defining the match.
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=NAME_MAX_LEN, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    start_datetime = models.DateTimeField(null=False)
    end_time = models.TimeField(auto_now=False)
    location = models.ForeignKey(MatchLocation, on_delete=models.CASCADE, null=False)
    min_age = models.IntegerField(default=MIN_AGE_DEFAULT)
    max_age = models.IntegerField(default=MAX_AGE_DEFAULT)
    min_rating = models.IntegerField(default=MIN_RATING_DEFAULT)
    private = models.BooleanField(default=PRIVATE_DEFAULT, null=False)

    # Whether the match is in the past.
    def is_in_past(self):
        return False

    # Model metadata.
    class Meta:
        verbose_name_plural = 'Matches'

    # A string representation of the match.
    def __str__(self):
        return self.name

# Represents a match participant. Also, represents a request.
class MatchParticipant(models.Model):

    # Defaults.
    ACCEPTED_DEFAULT = False

    # Attributes defining the match participant.
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=ACCEPTED_DEFAULT, null=False)

    # Model metadata.
    class Meta:
        verbose_name_plural = 'Match Participants'

    # Defines the name of the model.
    def __str__(self):
        return self.profile.user.username

# Defines the reasons for which a player can be reported.
class ReportReason(Enum):
    OFFENSIVE_LANGUAGE = 'Offensive Language'
    OFFENSIVE_BEHAVIOUR = 'Offensive Behaviour'
    RACISM = 'Racism'
    NO_SHOW = 'No Show'
    UNFAIR = 'Unfair'

# Defines a report; can only report in match. Multiple can be submited.
class MatchParticipantReport(models.Model):

    # Define model constants.
    REASON_MAX_LEN = 19
    REASON_DESC_MIN_LEN = 10
    REASON_DESC_MAX_LEN = 80

    # Attributes defining match report.
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporting_user')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user')
    reason = models.CharField(max_length=REASON_MAX_LEN, null=False, choices=[(tag, tag.value) for tag in ReportReason])
    desc = models.CharField(max_length=REASON_DESC_MAX_LEN, null=False)

    # Model metadata.
    class Meta:
        verbose_name_plural = 'Reported Participants'

    # A string representation of the report.
    def __str__(self):
        return self.id





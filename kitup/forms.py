import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from kitup.models import User, Profile, Sport, Match, Player, Report

# Form is used for the creation of djangos default User model.
# Thus, this form should be used for the creation of the user and 
# the associated profile.
class UserForm(forms.ModelForm):

    # Overwrite the User models fields.
    username = forms.CharField(min_length=Profile.USER_USERNAME_MIN_LENGTH, max_length=Profile.USER_USERNAME_MAX_LENGTH,
                               help_text='The name visible to other users of the site.')
    first_name = forms.CharField(help_text='Your first name; not visible to users.')
    last_name = forms.CharField(help_text='Your last name; not visible to users.')
    email = forms.EmailField(help_text='A valid email address associated with the account.')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Your account password - used for logging in.')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text='Confirm your password.')

    # The meta data class, defines the model and fields.
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    # We STILL need this function to check if passwords match. Refer to Django's form validation
    # Fixed it by adding the right clean_ prefix now.
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['confirm_password'] != cd['password']:
            raise forms.ValidationError("The passwords do not match!")

        return cd['confirm_password']

# Form defines the necessary fields for creating a match.
# Thus, this form should only be used when a match is being created or edited.
class MatchForm(forms.ModelForm):

    # Query the sports, permits the user to choose from a variety.
    SPORTS_CHOICES = [(sport.id, sport.name) for sport in Sport.objects.all()]

    # Define the fields that are required in order to create a match.
    sport = forms.ChoiceField(choices=SPORTS_CHOICES, help_text='Please select the sport for which the match is being '
                                                                'created.')
    name = forms.CharField(max_length=Match.NAME_MAX_LENGTH, help_text='Please enter the name of the match.')
    min_age = forms.IntegerField(initial=Match.DEFAULT_MIN_AGE, help_text='Please provide the minimum age a player '
                                                                          'can be in order to join the match.')
    max_age = forms.IntegerField(initial=Match.DEFAULT_MAX_AGE, help_text='Please provide the maximum age a player '
                                                                          'can be in order to join the match.')
    min_rating = forms.IntegerField(initial=Match.DEFAULT_MIN_RATING, help_text='Please provide the minimum rating a '
                                                                                'player must possess in order to join'
                                                                                ' the match.')

    # Meta class defines the model and the fields that are to be displayed.
    class Meta:
        model = Match
        fields = ('sport', 'name', 'min_age', 'max_age', 'min_rating')


# Form defines the necessary fields for creating a profile model.
# Thus, this from should be used for the creation of the user in conjunction
# with the UserForm form.
class ProfileForm(forms.ModelForm):

    # Form fields required in order to create a profile.
    profile_picture = forms.ImageField(help_text='Please provide a profile picture.')
    date_of_birth = forms.DateField(initial=datetime.date.today, help_text='Please specify your date of birth.')
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    strikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Defines the profile meta data i.e. models, fields etc.
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'profile_picture',)

# Form defines necessary fields required in order to create a report model.
# The from and to fields will be hidden given that they are extrapolated
# within the user_report view.
class ReportForm(forms.ModelForm):

    # Define the necessary fields in order to create a report.
    reason = forms.CharField(max_length=Report.REASON_MAX_LENGTH)

    # Defines the meta data for the report form.
    class Meta:
        model = Report
        fields = ('reason',)

# Defines a form that's to be used for logging in.
class UserLoginForm(forms.Form):

    # Profile the fields for logging in.
    username = forms.CharField(required=True,max_length=30,help_text='Account username.')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Account password.')

    # Meta class defines the visible form fields.
    class Meta:
        fields = ('username', 'password')



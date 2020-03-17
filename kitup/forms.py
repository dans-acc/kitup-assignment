import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from kitup.models import User, Profile, Sport, Match, Player, Report


'''
class UserForm(forms.ModelForm):

    # Overwrite the user models password field to hide it.
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    # Define the forms target model and the fields included / excluded.
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

        # Band aid fix for the 'required field text always showing'
        help_texts = {
            'username': '',
        }

    # Redefined the widgets in a 'non-redundant' way using the Form.fields attributes. This also helps us add CSS
    # Stuff if we need in the future
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})

    # We STILL need this function to check if passwords match. Refer to Django's form validation
    # Fixed it by adding the right clean_ prefix now.
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['confirm_password'] != cd['password']:
            raise forms.ValidationError("The passwords do not match!")

        return cd['confirm_password']

'''


# Form is used for the creation of djangos default User model.
# Thus, this form should be used for the creation of the user and 
# the associated profile.
class UserForm(forms.ModelForm):

    # Overwrite the User models fields.
    username = forms.CharField(min_length=Profile.USER_USERNAME_MIN_LENGTH, max_length=Profile.USER_USERNAME_MAX_LENGTH)
    first_name = forms.CharField(help_text='Please provide your first name')
    last_name = forms.CharField(help_text='Please provide the last name')
    email = forms.EmailField(help_text='Please provide an email address')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Please provide the password for the account.')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text='Please confirm the password.')

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
    sport = forms.ChoiceField(choices=SPORTS_CHOICES, help_text='Please select the sport for which the match is being created.')
    name = forms.CharField(max_length=Match.NAME_MAX_LENGTH, help_text='Please enter the name of the match.')
    min_age = forms.IntegerField(initial=Match.DEFAULT_MIN_AGE, help_text='Please provide the minimum age a player can be in order to join the match.')
    max_age = forms.IntegerField(initial=Match.DEFAULT_MAX_AGE, help_text='Please provide the maximum age a player can be in order to join the match.')
    min_rating = forms.IntegerField(initial=Match.DEFAULT_MIN_RATING, help_text='Please provide the minimum rating a player must possess in order to join the match.')
    team_home_score = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    team_away_score = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

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


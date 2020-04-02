import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.urls import reverse

from tempus_dominus import widgets as tdWidgets
from django.contrib.admin import widgets as adminWidgets

from kitup.models import Profile, Sport, MatchLocation, Match, MatchParticipant, MatchParticipantReport, ReportReason


# Form is used for the creation of djangos default User model.
# Thus, this form should be used for the creation of the user and 
# the associated profile.
class UserForm(forms.ModelForm):
    # Overwrite the User models fields.
    username = forms.CharField(min_length=Profile.USER_USERNAME_MIN_LEN, max_length=Profile.USER_USERNAME_MAX_LEN,
                               help_text='The name visible to other users of the site.')
    first_name = forms.CharField(help_text='Your first name; not visible to users.')
    last_name = forms.CharField(help_text='Your last name; not visible to users.')
    email = forms.EmailField(help_text='A valid email address associated with the account.')
    confirm_email = forms.EmailField(help_text='Confirm your email address.')
    password = forms.CharField(widget=forms.PasswordInput(),
                               help_text='Your account password - used for logging in. Minimum 8 characters required')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text='Confirm your password.')

    # The meta data class, defines the model and fields.
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'confirm_email', 'password', 'confirm_password')

    # We STILL need this function to check if passwords match. Refer to Django's form validation
    # Fixed it by adding the right clean_ prefix now.
    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['confirm_password'] != cd['password']:
            raise forms.ValidationError("The passwords do not match!")

        return cd['confirm_password']

    # Checks whether or not email exists in the database for a new user registering.
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        text = "This email address is already in use by another user. Please use <a href='%s'>Password Recovery</a> " \
               "if you can't login to your account" % reverse('kitup:password_reset')

        # Raises an error if an email already exists for a user.
        raise forms.ValidationError(mark_safe(text))

    # Verifies if the email addresses provided match or not.
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError("The emails do not match!")
        return cleaned_data


# Form is used to instantiate an instance of Match.
class MatchForm(forms.ModelForm):
    
    # Used to populate a pre-defined set of choices.
    #SPORTS_CHOICES = [(sport.id, sport.name) for sport in Sport.objects.all()]
    #LOCATION_CHOICES = [(location.id, f"{location.address}, {location.post_code}, {location.city} ({location.name})") for location in MatchLocation.objects.all()]

    # The fields that are utilised to create the match.
    sport_id = forms.ChoiceField( help_text='The sport for which the match is being held.')
    name = forms.CharField(max_length=Match.NAME_MAX_LEN, help_text='The name of the match.')
    start_datetime = forms.DateTimeField(
        widget=tdWidgets.DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
        help_text='Start date and time of the match.'
    )
    end_time = forms.TimeField(
        widget=tdWidgets.TimePicker(
            attrs={'input_toggle': True, 'input_group': False, }
        ),
        help_text='The time at which the match is expected to end.'
    )
    location_id = forms.ChoiceField( help_text='A trusted location at which the match will take place.')
    min_age = forms.IntegerField(initial=Match.MIN_AGE_DEFAULT, help_text='Minimum participating age.')
    max_age = forms.IntegerField(initial=Match.MAX_AGE_DEFAULT, help_text='Maximum participating age.')
    min_rating = forms.IntegerField(initial=Match.MIN_RATING_DEFAULT, help_text='The minimum rating of an attendee.')

    # Form metadata.
    class Meta:
        model = Match
        fields = ('sport_id', 'name', 'start_datetime', 'end_time', 'location_id', 'min_age', 'max_age', 'min_rating')


# Form defines the necessary fields for creating a profile model.
# Thus, this from should be used for the creation of the user in conjunction
# with the UserForm form.
class ProfileForm(forms.ModelForm):
    # Form fields required in order to create a profile.
    profile_picture = forms.ImageField(help_text='Please provide a profile picture.')
    date_of_birth = forms.DateField(
        widget=tdWidgets.DatePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
        initial=datetime.date.today,
        help_text='Please specify your date of birth.'
    )

    # Hidden fields that are used for internal purposes.
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    strikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Defines the profile meta data i.e. models, fields etc.
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'profile_picture',)

    '''
    # Checks whether or not the user has provided a date in the future or not
    def clean(self):
        data = super(ProfileForm, self).clean()
        current_date = datetime.date.today()

        if data['date_of_birth'] >= current_date:
            raise forms.ValidationError("You cannot choose a future date!")
        return self.data
    '''

# Form is submitted when reporting a match participant.
class MatchParticipantReportForm(forms.ModelForm):

    # The generalised reason for the report.
    reason = forms.ChoiceField(
        choices=[(tag, tag.value) for tag in ReportReason],
        help_text='Specify the reasoning for the report.')

    # The specific reasoning.
    desc = forms.CharField(
        widget=forms.Textarea(),
        min_length=MatchParticipantReport.REASON_DESC_MIN_LEN,
        max_length=MatchParticipantReport.REASON_DESC_MAX_LEN,
        help_text='Specify the reasoning for the report.')

    # From metadata.
    class Meta:
        model = MatchParticipantReport
        fields = ('reason', 'desc',)


# Defines a form that's to be used for logging in.
class UserLoginForm(forms.Form):
    # Profile the fields for logging in.
    username = forms.CharField(required=True, max_length=30, help_text='Account username.')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Account password.')

    # Meta class defines the visible form fields.
    class Meta:
        fields = ('username', 'password')



# Defines a form for the user to update their user specific information
class UserUpdateForm(forms.Form):
    email = forms.EmailField(help_text="Update your Email here.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Update your Password here.")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm your Update Password")

    class Meta:
        fields = ('email', 'password', 'password_confirm')


# Defines form for retrieving user email for password recovery
class EmailPasswordRecovery(forms.Form):
    email = forms.EmailField(required=True, help_text="Enter Email of Account")

    class Meta:
        fields = ('email')

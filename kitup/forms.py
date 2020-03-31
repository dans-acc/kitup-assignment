import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from tempus_dominus import widgets as tdWidgets
from django.contrib.admin import widgets as adminWidgets

from kitup.models import Profile, Sport, Match, MatchParticipant, PlayerReport


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
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Your account password - used for logging in. Minimum 8 characters required')
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

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

    # Checks whether or not email exists in the database for a new user registering.
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        # Raises an error if an email already exists for a user.
        raise forms.ValidationError('This email address is already in use. Please use Password Recovery if you cant login')


    # Verifies if the email addresses provided match or not.
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email:
            if email != confirm_email:
                raise forms.ValidationError("The emails do not match!")
        return cleaned_data


# MatchForm permits the creation of the Match model.
class MatchForm(forms.ModelForm):

    # The sports from which to select.
    #SPORTS_CHOICES = [(sport.id, sport.name) for sport in Sport.objects.all()]

    # The necessary fields that are used to create the match.
    sport = forms.ChoiceField(help_text='The sport for which the match is being held.')
    name = forms.CharField(max_length=Match.NAME_MAX_LEN, help_text='The name of the match.')

    # Match when and where fields, respectively - time and address. 
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
            attrs={'input_toggle': True, 'input_group': False,}
        ),
        help_text='The time at which the match is expected to end.'
    )

    # Match participant restriction fields - age and ranking limitations.
    min_age = forms.IntegerField(initial=Match.MIN_AGE_DEFAULT, help_text='Minimum participating age.')
    max_age = forms.IntegerField(initial=Match.MAX_AGE_DEFAULT, help_text='Maximum participating age.')
    min_rating = forms.IntegerField(initial=Match.MIN_RATING_DEFAULT, help_text='The minimum rating of an attendee.')

    # Meta class defines the model and the fields that are to be displayed.
    class Meta:
        model = Match
        fields = ('sport', 'name', 'start_datetime', 'end_time', 'min_age', 'max_age', 'min_rating')








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

    # Checks whether or not the user has provided a date in the future or not
    def clean(self):
        data = super(ProfileForm, self).clean()
        date_of_birth = data.get('date_of_birth')
        current_date = datetime.date.today()

        if date_of_birth >= current_date:
            raise forms.ValidationError("You cannot choose a future date!")
        return data



# Form defines necessary fields required in order to create a report model.
# The from and to fields will be hidden given that they are extrapolated
# within the user_report view.
class ReportForm(forms.ModelForm):

    # Define the necessary fields in order to create a report.
    reason = forms.CharField(max_length=PlayerReport.REASON_MAX_LEN)

    # Defines the meta data for the report form.
    class Meta:
        model = PlayerReport
        fields = ('reason',)


# Defines a form that's to be used for logging in.
class UserLoginForm(forms.Form):

    # Profile the fields for logging in.
    username = forms.CharField(required=True,max_length=30,help_text='Account username.')
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
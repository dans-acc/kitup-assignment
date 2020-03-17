from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from kitup.models import User, Profile, Sport, Match, Player, Report


# Form used to fill in the details for the user model.
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


# Define the form that is to be used for creating the profile.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'profile_picture',)

# Define the form that is used for the creation of a match.
class MatchForm(forms.ModelForm):

    # Define the match id's, names and owners.
    name = forms.CharField(max_length=Match.NAME_MAX_LENGTH, help_text='Please enter the name of the match.')

    # Define the minimum and maximum ages fields.
    min_age = forms.IntegerField(initial=Match.DEFAULT_MIN_AGE, help_text='Enter the minimum age a person must be in order to participate')
    max_age = forms.IntegerField(initial=Match.DEFAULT_MAX_AGE, help_text='Enter the maximum age a player can be in order to participate')

    # The rating field.
    min_rating = forms.IntegerField(initial=Match.DEFAULT_MIN_RATING, help_text='Enter the minimum rating required to join.')

    # Hide the team fields.
    team_home_score = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    team_away_score = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Meta class defines the model and the fields that are to be displayed.
    class Meta:
        model = Match
        fields = ('name', 'min_age', 'max_age', 'min_rating')

# Define the form that is used for the creation of a report.
class ReportForm(forms.ModelForm):

    # Define the maximum length of the reason.
    reason = forms.CharField(max_length=Report.REASON_MAX_LENGTH)

    class Meta:
        model = Report
        fields = ('reason',)



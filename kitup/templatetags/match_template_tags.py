from django import template
register = template.Library()

from kitup.models import Profile, Match, MatchParticipant

# Determines if the match is full.
@register.simple_tag
def is_match_full(match):
	try:
		return match.sport.max_participants <= MatchParticipant.objects.filter(match=match, accepted=True).count()
	except Match.DoesNotExist:
		return False

# Determines if the user is a match participant.
@register.simple_tag
def is_match_participant(match, user):
	try:
		profile = Profile.objects.get(user=user)
		return MatchParticipant.objects.get(profile=profile, match=match) is not None
	except MatchParticipant.DoesNotExist:
		return False

# Used to obtain the match owners profile.
@register.simple_tag
def get_match_owner_profile(user):
	try:
		return Profile.objects.get(user=user)
	except Profile.DoesNotExist:
		return None

@register.simple_tag
def get_match_participants(match, accepted):
	try:
		return MatchParticipant.objects.filter(match=match, accepted=accepted)
	except MatchParticipant.DoesNotExist:
		return None
	except Match.DoesNotExist:
		return None

# Get the participant instance for a given match.
@register.simple_tag
def get_match_participant(match, user):
	try:
		profile = Profile.objects.get(user=user)
		participant = MatchParticipant.objects.get(profile=profile, match=match)
		return participant
	except Profile.DoesNotExist:
		return None
	except Match.DoesNotExist:
		return None
	except MatchParticipant.DoesNotExist:
		return None
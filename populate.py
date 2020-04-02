import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kitup_project.settings')

import django

django.setup()
from django.contrib.auth.models import User


from kitup.models import Profile, Sport, Match, MatchParticipant, MatchLocation, MatchParticipantReport, ReportReason
from datetime import datetime, time, date


def populate():
    password = 'password123'

    # Setup users first
    users = [
        {
            'username': 'test1',
            'email': 'test1@test.com',
            'first_name': 'test',
            'last_name': 'one',
            'password': password
        },
        {
            'username': 'test2',
            'email': 'test2@test.com',
            'first_name': 'test',
            'last_name': 'two',
            'password': password
        },
        {
            'username': 'test3',
            'email': 'test3@test.com',
            'first_name': 'test',
            'last_name': 'three',
            'password': password
        }
    ]

    # setup the extra profile details
    profiles = [
        {
            'user_id': 1,
            'profile_picture': 'profile_images/test1.png',
            'date_of_birth': date(year=1989, month=3, day=25),
            'rating': 3.0,
            'reported': 0
        },
        {
            'user_id': 2,
            'profile_picture': 'profile_images/test2.png',
            'date_of_birth': date(year=1998, month=1, day=30),
            'rating': 1.5,
            'reported': 1
        },
        {
            'user_id': 3,
            'profile_picture': 'profile_images/test3.png',
            'date_of_birth': date(year=1999, month=8, day=23),
            'rating': 4.5,
            'reported': 0
        }
    ]

    # setup test sports
    sports = [
        {
            'name': '5-aside Football',
            'max_participants': 12,
            'sport_picture': 'sport_images/football.jpg'
        },
        {
            'name': '7-aside Football',
            'max_participants': 16,
            'sport_picture': 'sport_images/football.jpg'
        },
        {
            'name': '11-aside Football',
            'max_participants': 24,
            'sport_picture': 'sport_images/football.jpg'
        }
    ]

    # Setup Match locations
    locations = [
        {
            'name': 'Stevenson Building',
            'address': '77 Oakfield Avenue',
            'post_code': 'G12 8LT',
            'city': 'Glasgow',
            'latitude': 4.2857,
            'longitude': 55.8726
        },
        {
            'name': 'Garscube Sports Complex',
            'address': 'West of Scotland Science Park',
            'post_code': 'G20 0SP',
            'city': 'Glasgow',
            'latitude': 4.3129,
            'longitude': 55.8998
        }
    ]

    # Setup test Matches
    matches = [
        {
            'name': 'Bobs return',
            'start_datetime': datetime(year=2020, month=4, day=25,  hour=21,
                                       minute=0, second=0),
            'end_time': time(hour=22, minute=00, second=00),
            'min_age': 20,
            'max_age': 25,
            'private': 0,
            'location_id': 1,
            'owner_id': 2,
            'sport_id': 2
        },
        {
            'name': 'revenge',
            'start_datetime': datetime(year=2020, month=7, day=25,
                                       hour=21, minute=00, second=00),
            'end_time': time(hour=22,minute=00, second=00),
            'min_age': 20,
            'max_age': 35,
            'private': 0,
            'location_id': 2,
            'owner_id': 3,
            'sport_id': 1
        }
    ]

    participants = [
        {
            'accepted': 0,
            'match_id': 1,
            'profile_id': 2
        },
        {
            'accepted': 1,
            'match_id': 1,
            'profile_id': 3
        },
        {
            'accepted': 1,
            'match_id': 2,
            'profile_id': 2
        },
        {
            'accepted': 0,
            'match_id': 2,
            'profile_id': 3
        },
    ]

    reports = [
        {
            'reason': ReportReason.NO_SHOW,
            'desc': '',
            'match_id': 1,
            'reported_user_id': 2,
            'reporting_user_id': 1
        },
        {
            'reason': ReportReason.OFFENSIVE_BEHAVIOUR,
            'desc': 'Was committing to many hard tackles',
            'match_id': 2,
            'reported_user_id': 2,
            'reporting_user_id': 3
        },
    ]

    # Iterate through users and call populate users to add to users table
    for user in users:
        u = populate_users(user['username'], user['email'], user['first_name'],
                           user['last_name'], user['password'])

    # Iterate through profiles and call populate profiles to add extra user data to profile table
    for profile in profiles:
        p = populate_profiles(profile['user_id'], profile['profile_picture'],
                              profile['date_of_birth'], profile['rating'], profile['reported'])

    # Iterate through sports
    for sport in sports:
        s = populate_sports(sport['name'], sport['max_participants'], sport['sport_picture'])

    # Iterate through locations
    for location in locations:
        l = populate_match_locations(location['name'], location['address'], location['post_code'],
                                     location['city'], location['latitude'], location['longitude'])

    # Iterate through matches
    for match in matches:
        m = populate_matches(match['name'], match['start_datetime'], match['end_time'],
                             match['min_age'], match['max_age'], match['private'],
                             match['location_id'], match['owner_id'], match['sport_id'])

    # Iterate through participants
    for participant in participants:
        ps = populate_match_participants(participant['accepted'], participant['match_id'],
                                         participant['profile_id'])

    # Iterate through reports
    #for report in reports:
     #   r = populate_match_report(report['reason'], report['desc'], report['match_id'],
      #                            report['reported_user_id'], report['reporting_user_id'])


# Function for populating the users table
def populate_users(username, email, first_name, last_name, password):
    user = User()
    user = User.objects.get_or_create(username=username, email=email,
                                      first_name=first_name, last_name=last_name)[0]
    user.set_password(raw_password=password)
    user.save()
    return user


# Function for populating teh profile table
def populate_profiles(user_id, profile_picture, date_of_birth, rating, reported):
    profile = Profile.objects.get_or_create(user_id=user_id, profile_picture=profile_picture,
                                            date_of_birth=date_of_birth, rating=rating,
                                            reported=reported)[0]
    profile.save()
    return profile


# Function for populating the sport table
def populate_sports(name, max_participants, sport_picture):
    sport = Sport.objects.get_or_create(name=name, max_participants=max_participants,
                                        sport_picture=sport_picture)[0]
    sport.save()
    return sport


# Function to populate the macth location table
def populate_match_locations(name, address, postcode, city, latitude, longitude):
    location = MatchLocation.objects.get_or_create(name=name, address=address,
                                                   post_code=postcode, city=city,
                                                   latitude=latitude, longitude=longitude)[0]
    location.save()
    return location


# Function for populating match table
def populate_matches(name, start_datetime, end_time, min_age, max_age, private, location_id, owner_id, sport_id):
    match = Match.objects.get_or_create(name=name, start_datetime=start_datetime, end_time=end_time,
                                        min_age=min_age, max_age=max_age, private=private,
                                        location_id=location_id, owner_id=owner_id, sport_id=sport_id)[0]
    match.save()
    return match


# Function for populating the match participants table
def populate_match_participants(accepted, match_id, profile_id):
    participant = MatchParticipant.objects.get_or_create(accepted=accepted, match_id=match_id,
                                                         profile_id=profile_id)[0]
    participant.save()
    return participant


# function for populating match report table
def populate_match_report(reason, desc, match_id, reported_user_id, reporting_user_id):
    report = MatchParticipantReport.objects.get_or_create(reason=reason, desc=desc, match_id=match_id,
                                                          reported_user_id=reported_user_id,
                                                          reporting_user_id=reporting_user_id)[0]
    report.save()
    return report


if __name__ == '__main__':
    print('Starting populate script')
    populate()

import os

from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kitup_project.settings')

import django

django.setup()

from kitup.models import Profile, Player, Match, Sport, Report

# Password hashing
import bcrypt


def populate():
    pass1 = b'simpson'
    pass2 = b'vailjevs'
    pass3 = b'shehabi'

    profiles = [
        {'forename': 'James',
         'surname': 'simpson',
         'password': bcrypt.hashpw(password=pass1, salt=bcrypt.gensalt()),
         'age': 23},
        {'forename': 'Daniels',
         'surname': 'Vasiljevs',
         'password': bcrypt.hashpw(password=pass2, salt=bcrypt.gensalt()),
         'age': 23},
        {'forename': 'Basel',
         'surname': 'Shehabi',
         'password': bcrypt.hashpw(password=pass3, salt=bcrypt.gensalt())}
    ]

    sports = [
        {'name': '5-aside Football',
         'team_size': 5}
    ]

    matches = [
        {'name': 'Big Davies sess',
         'sport_id': 1,
         'min_age': 18,
         'max_age': 25,
         'min_rating': 3,
         'date': '25/03/2020',
         'time': '20:00',
         'duration': '60'}
    ]

    players = [
        {'player_id': 1,
         'game_id': 1,
         'team': 1},
        {'player_id': 2,
         'game_id': 1,
         'team': 2},
        {'player_id': 3,
         'game_id': 1,
         'team': 2}
    ]

    reports = [
        {'report_maker': 1,
         'report_subject': 2,
         'reason': 'An Asshole'},
        {'report_maker': 3,
         'report_subject': 2,
         'reason': 'An Asshole'}
    ]

    for profile in profiles:
        u = add_profile(profile)
    for sport in sports:
        s = add_sport(sport)
    for match in matches:
        m = add_match(match)
    for player in players:
        p = add_player(player)
    for report in reports:
        r = add_report(report)


def add_profile(profile):
    print(profile)
    User.objects.create_user(profile['forename'],
                             profile['surname'],
                             profile['password'])
    u = Profile.objects.get_or_create(age=profile['age'])[0]
    u.save()
    return u


def add_sport(sport):
    s = Sport.objects.get_or_create(sport=sport)[0]
    s.save()
    return s


def add_match(match):
    m = Match.objects.get_or_create(match=match)[0]
    m.save()
    return m


def add_player(player):
    p = Player.objects.get_or_create(player=player)[0]
    p.save()
    return p


def add_report(report):
    r = Report.objects.get_or_create(report=report)[0]
    r.save()
    return r


if __name__ == '__main__':
    print("Starting population Script")
    populate()

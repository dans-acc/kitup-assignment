import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kitup_project.settings')


import django
django.setup()

from kitup.models import Users, Player, Match, Sport, Report

# Password hashing
import bcrypt


def populate():

    salt = 'Hg4'
    pass1 = 'simpson'.encode('utf-8')
    pass2 = 'vailjevs'.encode('utf-8')
    pass3 = 'shehabi'.encode('utf-8')

    users = [
        {'forename': 'James',
         'surname': 'simpson',
         'password': bcrypt.hashpw(password=pass1, salt=salt),
         'age': 23},
        {'forename': 'Daniels',
         'surname': 'Vasiljevs',
         'password': bcrypt.hashpw(password=pass2, salt=salt),
         'age': 23},
        {'forename': 'Basil',
         'surname': 'Shehabi',
         'password': bcrypt.hashpw(password=pass3, salt=salt)}
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

    for user in users:
        u = add_user(user)
    for sport in sports:
        s = add_sport(sport)
    for match in matches:
        m = add_match(match)
    for player in players:
        p = add_player(player)
    for report in reports:
        r = add_report(report)


def add_user(user):
    u = Users.objects.get_or_create(user=user)[0]
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
    r = Report.obkects.get_or_create(report=report)[0]
    r.save()
    return r


if __name__ == '__main__':
    print("Starting population Script")
    populate()


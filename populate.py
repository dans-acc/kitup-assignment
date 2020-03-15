import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kitup_project.settings')

import django
django.setup()

from kitup.models import Users, Player, Match, Sport, Report

def populate():

    users = [
        {'forename': 'James',
         'surname': 'simpson',
         }
    ]
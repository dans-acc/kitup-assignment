# Generated by Django 3.0.4 on 2020-04-01 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kitup.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('start_datetime', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('min_age', models.IntegerField(default=14)),
                ('max_age', models.IntegerField(default=70)),
                ('min_rating', models.IntegerField(default=0)),
                ('private', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='MatchLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=40)),
                ('post_code', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=30)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('max_participants', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Sports',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(upload_to='profile_images')),
                ('date_of_birth', models.DateField()),
                ('rating', models.FloatField(default=0)),
                ('reported', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='MatchParticipantReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[(kitup.models.ReportReason['OFFENSIVE_LANGUAGE'], 'Offensive Language'), (kitup.models.ReportReason['OFFENSIVE_BEHAVIOUR'], 'Offensive Behaviour'), (kitup.models.ReportReason['RACISM'], 'Racism'), (kitup.models.ReportReason['NO_SHOW'], 'No Show'), (kitup.models.ReportReason['UNFAIR'], 'Unfair')], max_length=19)),
                ('desc', models.CharField(max_length=80)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitup.Match')),
                ('reported_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to=settings.AUTH_USER_MODEL)),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Player Reports',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitup.MatchLocation'),
        ),
        migrations.AddField(
            model_name='match',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitup.Sport'),
        ),
        migrations.CreateModel(
            name='MatchParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitup.Match')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitup.Profile')),
            ],
            options={
                'verbose_name_plural': 'Match Participants',
                'unique_together': {('profile', 'match')},
            },
        ),
    ]

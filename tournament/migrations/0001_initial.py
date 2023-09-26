# Generated by Django 4.2 on 2023-09-03 12:42

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EliminationMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elimination_mode', models.CharField(choices=[('Single Elimination', 'Single Elimination'), ('Double Elimination', 'Double Elimination'), ('Battle Royale', 'Battle Royale'), ('Round Robbin', 'Round Robbin')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=700)),
                ('event_name', models.CharField(max_length=700, unique=True)),
                ('event_thumbnail', models.FileField(blank=True, upload_to='')),
                ('event_thumbnail_alt_description', models.CharField(blank=True, max_length=500)),
                ('event_description', ckeditor.fields.RichTextField(blank=True)),
                ('event_start_date', models.DateTimeField()),
                ('event_end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=500)),
                ('game_image', models.FileField(upload_to='')),
                ('game_type', models.CharField(choices=[('PC', 'PC'), ('Mobile', 'Mobile')], default='Mobile', max_length=100)),
                ('elimination_modes', models.ManyToManyField(to='tournament.eliminationmode')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_number', models.IntegerField()),
                ('stage_name', models.CharField(max_length=500)),
                ('input_no_of_teams', models.IntegerField()),
                ('output_no_of_teams', models.IntegerField()),
                ('stage_elimation_mode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.eliminationmode')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=500)),
                ('team_image', models.FileField(upload_to='')),
                ('team_type', models.CharField(choices=[('Duo', 'Duo'), ('Squad', 'Squad')], default='Squad', max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.game')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.organization')),
                ('players', models.ManyToManyField(blank=True, related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('tournament_name', models.CharField(max_length=700)),
                ('tournament_logo', models.FileField(blank=True, upload_to='')),
                ('tournament_banner', models.FileField(blank=True, upload_to='')),
                ('tournament_mode', models.CharField(choices=[('Online', 'Online'), ('LAN', 'LAN')], default='Online', max_length=700)),
                ('tournament_status', models.CharField(choices=[('Live', 'Live'), ('Past', 'Past'), ('Upcoming', 'Upcoming')], default='Upcoming', max_length=50)),
                ('tournament_participants', models.CharField(choices=[('Player', 'Player'), ('Team', 'Team')], default='Team', max_length=700)),
                ('is_free', models.BooleanField(default=False)),
                ('tournament_fee', models.FloatField(blank=True, null=True)),
                ('maximum_no_of_participants', models.IntegerField(default=0)),
                ('tournament_description', ckeditor.fields.RichTextField(blank=True)),
                ('tournament_short_description', models.CharField(blank=True, max_length=150)),
                ('tournament_rules', ckeditor.fields.RichTextField(blank=True)),
                ('tournament_prize_pool', ckeditor.fields.RichTextField(blank=True)),
                ('registration_opening_date', models.DateTimeField(blank=True, null=True)),
                ('registration_closing_date', models.DateTimeField(blank=True, null=True)),
                ('tournament_start_date', models.DateTimeField(blank=True, null=True)),
                ('tournament_end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_registration_enabled', models.BooleanField(default=False)),
                ('accept_registration_automatic', models.BooleanField(default=False)),
                ('contact_email', models.CharField(blank=True, max_length=500)),
                ('discord_link', models.URLField(blank=True, max_length=500)),
                ('is_verified', models.BooleanField(default=False)),
                ('no_of_participants', models.IntegerField(default=0)),
                ('live_link', models.TextField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='tournament.event')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='tournament.game')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentStreams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_title', models.CharField(max_length=500)),
                ('url', models.URLField(max_length=500)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streams', to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentSponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=500)),
                ('sponsor_link', models.CharField(blank=True, max_length=500)),
                ('sponsorship_category', models.CharField(max_length=500)),
                ('sponsor_banner', models.FileField(upload_to='')),
                ('order', models.IntegerField(default=0)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('heading', models.CharField(max_length=1000)),
                ('detail', models.TextField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TeamTournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('registration_status', models.CharField(choices=[('Ongoing Review', 'Ongoing Review'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Ongoing Review', max_length=500)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Esewa', 'Esewa'), ('Khalti', 'Khalti'), ('Other', 'Other')], default='Other', max_length=500)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_registrations', to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1_points', models.FloatField()),
                ('team2_points', models.FloatField()),
                ('team1_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW'), ('ABORTED', 'ABORTED'), ('ABORTED', 'ABORTED')], max_length=500)),
                ('team2_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW'), ('ABORTED', 'ABORTED'), ('ABORTED', 'ABORTED')], max_length=500)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team1', to='tournament.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team2', to='tournament.team')),
            ],
        ),
        migrations.AddField(
            model_name='stage',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament'),
        ),
        migrations.CreateModel(
            name='SoloTournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('registration_fee', models.FloatField()),
                ('registration_status', models.CharField(choices=[('Ongoing Review', 'Ongoing Review'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Ongoing Review', max_length=500)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Esewa', 'Esewa'), ('Other', 'Other')], default='Other', max_length=500)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_registrations', to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='SoloMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_points', models.FloatField()),
                ('player2_points', models.FloatField()),
                ('player1_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('player2_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player2', to=settings.AUTH_USER_MODEL)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
            ],
        ),
        migrations.CreateModel(
            name='SingleEliminationRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_name', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('number_of_matches', models.IntegerField(blank=True, null=True)),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
            ],
        ),
        migrations.CreateModel(
            name='SingleEliminationMatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_name', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('round', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.singleeliminationround')),
                ('team1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='SingleEliminationTeam1', to='tournament.team')),
                ('team2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='SingleEliminationTeam2', to='tournament.team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner', to='tournament.team')),
            ],
        ),
        migrations.CreateModel(
            name='EventSponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=500)),
                ('sponsorship_category', models.CharField(max_length=500)),
                ('sponsor_banner', models.FileField(upload_to='')),
                ('order', models.IntegerField(default=0)),
                ('sponsor_link', models.CharField(blank=True, max_length=500)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventNewsFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='EventFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('heading', models.CharField(max_length=1000)),
                ('detail', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
            ],
        ),
        migrations.CreateModel(
            name='DoubleEliminationRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_name', models.CharField(blank=True, max_length=500, null=True)),
                ('bracket', models.CharField(choices=[('WB', 'WB'), ('LB', 'LB')], default='WB', max_length=500)),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('number_of_matches', models.IntegerField(blank=True, null=True)),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
            ],
        ),
        migrations.CreateModel(
            name='DoubleEliminationMatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_name', models.CharField(blank=True, max_length=500, null=True)),
                ('start_date_time', models.DateTimeField(blank=True, null=True)),
                ('round', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.doubleeliminationround')),
                ('team1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DoubleEliminationTeam1', to='tournament.team')),
                ('team2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DoubleEliminationTeam2', to='tournament.team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DoubleEliminationMatchWinner', to='tournament.team')),
            ],
        ),
    ]

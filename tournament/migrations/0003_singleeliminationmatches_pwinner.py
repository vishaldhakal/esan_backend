# Generated by Django 4.2 on 2023-09-05 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0002_doubleeliminationmatches_player1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleeliminationmatches',
            name='pWinner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='player_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]

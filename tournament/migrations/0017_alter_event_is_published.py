# Generated by Django 4.2 on 2023-06-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0016_alter_solotournamentregistration_tournament_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]

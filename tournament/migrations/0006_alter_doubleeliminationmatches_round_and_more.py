# Generated by Django 4.2 on 2023-09-07 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_tournamentprizepool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubleeliminationmatches',
            name='round',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tournament.doubleeliminationround'),
        ),
        migrations.AlterField(
            model_name='doubleeliminationround',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.stage'),
        ),
        migrations.AlterField(
            model_name='singleeliminationmatches',
            name='round',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tournament.singleeliminationround'),
        ),
        migrations.AlterField(
            model_name='singleeliminationround',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.stage'),
        ),
    ]

# Generated by Django 4.2 on 2023-05-13 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('post', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('facebook_link', models.CharField(blank=True, max_length=250)),
                ('instagram_link', models.CharField(blank=True, max_length=250)),
                ('twitch_link', models.CharField(blank=True, max_length=250)),
                ('discord_link', models.CharField(blank=True, max_length=250)),
                ('twitter_link', models.CharField(blank=True, max_length=250)),
                ('linkedin_link', models.CharField(blank=True, max_length=250)),
            ],
        ),
    ]

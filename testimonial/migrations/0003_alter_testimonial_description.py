# Generated by Django 4.2 on 2023-05-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonial', '0002_alter_testimonial_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]

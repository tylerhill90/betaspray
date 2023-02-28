# Generated by Django 4.1.7 on 2023-02-26 17:30

from django.conf import settings
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('walls', '0002_alter_route_wall_alter_routehold_route_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='wall',
            unique_together={('owner', 'name')},
        ),
    ]
# Generated by Django 3.1.4 on 2020-12-10 20:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0011_auto_20201210_2305'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_followers',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'following')},
        ),
    ]

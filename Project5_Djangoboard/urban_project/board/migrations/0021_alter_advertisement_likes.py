# Generated by Django 5.0.3 on 2024-12-04 16:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0020_alter_advertisement_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='likes',
            field=models.ManyToManyField(related_name='Advertisement', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 5.0.3 on 2024-12-02 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_alter_advertisement_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='picture',
        ),
    ]
# Generated by Django 5.0.3 on 2024-12-02 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='picture',
            field=models.ImageField(default=1, upload_to=None),
            preserve_default=False,
        ),
    ]

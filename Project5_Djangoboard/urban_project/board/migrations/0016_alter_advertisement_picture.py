# Generated by Django 5.0.3 on 2024-12-02 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_advertisement_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='picture',
            field=models.ImageField(default='img/default.jpg', null=True, upload_to='img'),
        ),
    ]
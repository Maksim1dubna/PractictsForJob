# Generated by Django 5.0.3 on 2024-12-02 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_advertisement_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='picture',
            field=models.ImageField(default='img/default.jpg', upload_to='img/'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-12-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_advertisement_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='picture',
            field=models.ImageField(upload_to='img/'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-12-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_alter_advertisement_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='picture',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]

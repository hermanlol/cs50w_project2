# Generated by Django 3.2.7 on 2021-11-02 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211102_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='picture',
            field=models.FileField(blank=True, default=None, upload_to=''),
        ),
    ]

# Generated by Django 3.2.7 on 2021-11-02 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listings_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='current_bid',
            field=models.FloatField(null=True),
        ),
    ]
# Generated by Django 4.2.6 on 2023-11-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_bidding_delete_bidding1_delete_bidding2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding',
            name='bid_text',
            field=models.CharField(max_length=19999),
        ),
    ]

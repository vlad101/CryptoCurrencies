# Generated by Django 3.1.5 on 2021-01-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinmarketdata',
            name='top_tier_volume',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
        migrations.AddField(
            model_name='coinmarketdata',
            name='total_volume',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
        migrations.AlterField(
            model_name='coinmarketdata',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptocurrencies', '0002_auto_20210106_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coinmarketdata',
            options={'verbose_name_plural': 'Coin Market Data'},
        ),
        migrations.AddField(
            model_name='coinmarketdata',
            name='direct_volume',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
        migrations.AddField(
            model_name='coinmarketdata',
            name='market_cap',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
    ]

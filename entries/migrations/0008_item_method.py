# Generated by Django 4.0.4 on 2022-07-02 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0007_item_period_month_item_period_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='method',
            field=models.CharField(default='E', max_length=1),
        ),
    ]

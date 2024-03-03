# Generated by Django 4.0.4 on 2024-03-02 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0012_remove_person_attendance_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(verbose_name=datetime.date(2024, 3, 9)),
        ),
    ]

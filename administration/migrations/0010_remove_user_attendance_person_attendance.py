# Generated by Django 4.0.4 on 2023-04-06 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0009_user_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='attendance',
        ),
        migrations.AddField(
            model_name='person',
            name='attendance',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

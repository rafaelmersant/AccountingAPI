# Generated by Django 4.0.4 on 2022-04-22 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_remove_concept_location_user_username'),
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='reference',
            new_name='note',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='concept',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='type',
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18, null=True)),
                ('reference', models.CharField(max_length=255)),
                ('type', models.CharField(default='E', max_length=1)),
                ('concept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.concept')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.entry')),
            ],
        ),
    ]

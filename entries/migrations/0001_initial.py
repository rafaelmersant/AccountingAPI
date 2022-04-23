# Generated by Django 4.0.4 on 2022-04-21 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18, null=True)),
                ('reference', models.CharField(max_length=255)),
                ('type', models.CharField(default='E', max_length=1)),
                ('period_month', models.PositiveSmallIntegerField()),
                ('period_year', models.PositiveSmallIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('church', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.church')),
                ('concept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.concept')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.user')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.person')),
            ],
        ),
    ]
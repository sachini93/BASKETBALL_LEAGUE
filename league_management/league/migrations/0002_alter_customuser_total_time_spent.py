# Generated by Django 5.0.6 on 2024-06-22 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='total_time_spent',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
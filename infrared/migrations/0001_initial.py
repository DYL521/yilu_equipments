# Generated by Django 2.0.7 on 2018-07-17 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Infrared',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('manufacture', models.SmallIntegerField(choices=[(0, 'hao shi lai'), (10, 'bang qi')])),
                ('manufacture_device_id', models.CharField(max_length=256)),
                ('human_detected', models.BooleanField(default=True)),
                ('last_time_human_detected', models.DateTimeField(blank=True, null=True)),
                ('position', models.SmallIntegerField(choices=[
                 (0, 'just in door'), (10, 'in toilet'), (20, 'in bed room'), (100, 'other')])),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='room.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

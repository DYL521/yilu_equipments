# Generated by Django 2.1.1 on 2018-10-18 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Door',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('manufacture', models.SmallIntegerField(choices=[(0, 'haolishi'), (10, 'bang qi'), (9999999, 'dummy')])),
                ('manufacture_device_id', models.CharField(max_length=256)),
                ('is_opened', models.NullBooleanField(default=None)),
                ('open_direction', models.SmallIntegerField(choices=[(0, 'not sure'), (10, 'from inside'), (20, 'from outside')], default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='room.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DoorSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('manufacture', models.SmallIntegerField(choices=[(0, 'haolishi'), (10, 'bang qi'), (9999999, 'dummy')])),
                ('manufacture_device_id', models.CharField(max_length=256)),
                ('is_opened', models.NullBooleanField(default=None)),
                ('open_method', models.SmallIntegerField(choices=[(0, 'not sure'), (10, 'hotel card'), (20, 'ID card'), (30, 'facial recognization'), (40, 'password')], default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='room.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('manufacture', models.SmallIntegerField(choices=[(0, 'haolishi'), (10, 'bang qi'), (9999999, 'dummy')])),
                ('manufacture_device_id', models.CharField(max_length=256)),
                ('is_opened', models.NullBooleanField(default=None)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='room.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserUnlockTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('card_type', models.SmallIntegerField(choices=[(0, 'not sure'), (10, 'hotel card'), (20, 'ID card'), (30, 'facial recognization'), (40, 'password')], default=0)),
                ('card_data', models.CharField(max_length=256)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='room.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

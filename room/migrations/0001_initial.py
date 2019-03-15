# Generated by Django 2.0.6 on 2018-06-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('hid', models.IntegerField(help_text='Hotel ID from EFD_set')),
                ('room_number', models.CharField(max_length=16)),
                ('floor', models.SmallIntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[
                 (0, 'available'), (10, 'inuse'), (20, 'cleaning'), (30, 'maintaining')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# Generated by Django 2.1.1 on 2018-10-18 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('air_conditioner', '0003_remove_airconditioner_room_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airconditioner',
            name='manufacture',
            field=models.SmallIntegerField(choices=[(0, 'haolishi'), (10, 'bang qi'), (9999999, 'dummy')]),
        ),
    ]

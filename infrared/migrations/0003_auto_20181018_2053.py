# Generated by Django 2.1.1 on 2018-10-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrared', '0002_auto_20181016_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infrared',
            name='manufacture',
            field=models.SmallIntegerField(choices=[(0, 'hao_li_shi'), (10, 'bang_qi'), (9999999, 'dummy')]),
        ),
    ]

# Generated by Django 2.1 on 2018-12-12 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cateye', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cateye',
            name='manufacture',
            field=models.SmallIntegerField(choices=[(0, 'hao_li_shi'), (10, 'bang_qi'), (20, 'yi lu'), (30, 'samsung_air_conditioner'), (9999999, 'dummy')]),
        ),
    ]

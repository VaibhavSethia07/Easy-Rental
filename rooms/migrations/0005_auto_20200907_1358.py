# Generated by Django 2.2.5 on 2020-09-07 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200907_0336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roomtype',
            options={'verbose_name': 'Room Type'},
        ),
        migrations.AddField(
            model_name='roomtype',
            name='subtitle',
            field=models.CharField(max_length=140, null=True),
        ),
    ]

# Generated by Django 2.1.4 on 2019-04-15 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0009_usernovel'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='hot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usernovel',
            name='praise',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usernovel',
            name='user_name',
            field=models.CharField(default='anoymous', max_length=150),
        ),
    ]
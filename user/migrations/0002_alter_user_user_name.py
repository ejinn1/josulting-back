# Generated by Django 4.2.1 on 2023-05-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=16, verbose_name='유저 이름'),
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-10 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0005_remove_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='c4_exp',
            field=models.IntegerField(default=90),
        ),
    ]
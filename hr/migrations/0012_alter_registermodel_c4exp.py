# Generated by Django 4.2.3 on 2023-08-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0011_alter_registermodel_c4exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='c4Exp',
            field=models.IntegerField(blank=True, default='365', null='True'),
        ),
    ]

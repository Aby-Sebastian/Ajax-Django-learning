# Generated by Django 3.1.7 on 2021-07-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210707_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='link_only_ip_address',
            name='country',
            field=models.CharField(default='India', max_length=50),
        ),
    ]

# Generated by Django 2.2.6 on 2019-10-22 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191017_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_restaurant',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]

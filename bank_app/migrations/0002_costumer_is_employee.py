# Generated by Django 3.1.6 on 2021-03-09 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='costumer',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
    ]

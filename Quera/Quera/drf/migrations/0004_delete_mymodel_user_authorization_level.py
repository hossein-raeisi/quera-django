# Generated by Django 5.0.6 on 2024-07-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf', '0003_usertoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyModel',
        ),
        migrations.AddField(
            model_name='user',
            name='authorization_level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

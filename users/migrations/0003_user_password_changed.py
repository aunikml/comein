# Generated by Django 5.1.4 on 2025-01-01 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_changed',
            field=models.BooleanField(default=False),
        ),
    ]
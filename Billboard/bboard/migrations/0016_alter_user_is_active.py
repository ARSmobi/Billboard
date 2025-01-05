# Generated by Django 5.0.6 on 2025-01-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0015_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting account.', verbose_name='active'),
        ),
    ]
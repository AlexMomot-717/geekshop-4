# Generated by Django 3.2.8 on 2021-11-19 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20211118_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopuser',
            old_name='activation_key',
            new_name='activate_key',
        ),
        migrations.RenameField(
            model_name='shopuser',
            old_name='activation_key_expires',
            new_name='activate_key_expires',
        ),
    ]
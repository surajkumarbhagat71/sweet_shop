# Generated by Django 2.2.7 on 2020-09-04 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order',
            new_name='order_time',
        ),
    ]

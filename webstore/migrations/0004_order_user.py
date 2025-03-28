# Generated by Django 5.1.7 on 2025-03-08 21:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def set_default_user(apps, schema_editor):
    Order = apps.get_model('webstore', 'Order')
    User = apps.get_model('auth', 'User')
    default_user = User.objects.first()  # Get the first user as the default
    if default_user:
        Order.objects.all().update(user=default_user)


class Migration(migrations.Migration):

    dependencies = [
        ('webstore', '0003_alter_menu_img_url_notification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                default=1,  # Temporary default value
            ),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_user),  # Populate the user field
    ]

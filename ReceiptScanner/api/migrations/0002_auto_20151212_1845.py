# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='image',
            new_name='names_image',
        ),
        migrations.AddField(
            model_name='receipt',
            name='prices_image',
            field=models.ImageField(default=datetime.datetime(2015, 12, 12, 18, 45, 55, 222090, tzinfo=utc), upload_to='prices/'),
            preserve_default=False,
        ),
    ]

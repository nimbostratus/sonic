# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoutbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shout',
            options={'ordering': ('-created_at',)},
        ),
    ]

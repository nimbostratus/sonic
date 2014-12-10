# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20141210_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='icon',
            field=models.CharField(max_length=12, null=True, verbose_name='icon', blank=True),
            preserve_default=True,
        ),
    ]

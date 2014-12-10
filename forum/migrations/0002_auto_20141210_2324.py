# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='icon',
            field=models.CharField(max_length=10, null=True, verbose_name='icon', blank=True),
            preserve_default=True,
        ),
    ]

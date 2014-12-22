# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='activation_hash_md5',
            field=models.CharField(max_length=32, null=True, verbose_name='activation hash', blank=True),
            preserve_default=True,
        ),
    ]

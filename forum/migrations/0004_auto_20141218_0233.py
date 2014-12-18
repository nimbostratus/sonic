# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20141210_2326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'ordering': ('-order',)},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-order',)},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='board',
            name='parent',
            field=models.ForeignKey(related_name='child_set', blank=True, to='forum.Board', null=True),
            preserve_default=True,
        ),
    ]

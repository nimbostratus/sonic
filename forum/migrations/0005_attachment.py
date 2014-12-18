# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20141218_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'attachments/', verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(to='forum.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

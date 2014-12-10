# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0, verbose_name='sort order')),
                ('name', models.CharField(max_length=120, verbose_name='category')),
                ('description', models.CharField(max_length=250, verbose_name='category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='category')),
                ('order', models.IntegerField(default=0, verbose_name='sort order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at', null=True)),
                ('subject', models.CharField(max_length=120, verbose_name='category')),
                ('body', models.TextField(verbose_name='body')),
                ('icon', models.CharField(max_length=2, null=True, verbose_name='icon', blank=True)),
                ('created_by', models.ForeignKey(related_name='post_created_set', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='post_modified_set', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_sticky', models.BooleanField(default=False, verbose_name='is sticky')),
                ('board', models.ForeignKey(to='forum.Board')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(to='forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='board',
            name='category',
            field=models.ForeignKey(to='forum.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='board',
            name='parent',
            field=models.ForeignKey(blank=True, to='forum.Board', null=True),
            preserve_default=True,
        ),
    ]

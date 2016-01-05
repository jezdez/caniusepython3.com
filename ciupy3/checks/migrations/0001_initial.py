# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pg.models.fields.uuid
import django_pg.models.fields.datetime_
import django_pg.models.fields.array
import django_pg.models.fields.json
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(primary_key=True, editable=False, unique=True, serialize=False)),
                ('unblocked', models.SmallIntegerField(default=0)),
                ('created_at', django_pg.models.fields.datetime_.DateTimeField(default=django.utils.timezone.now)),
                ('started_at', django_pg.models.fields.datetime_.DateTimeField(null=True, blank=True)),
                ('finished_at', django_pg.models.fields.datetime_.DateTimeField(null=True, blank=True)),
                ('requirements', django_pg.models.fields.array.ArrayField(null=True)),
                ('projects', django_pg.models.fields.array.ArrayField(null=True)),
                ('blockers', django_pg.models.fields.json.JSONField(default=None, null=True, blank=True)),
                ('public', models.BooleanField(default=True)),
                ('runs', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ('-finished_at',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(primary_key=True, editable=False, unique=True, serialize=False)),
                ('name', models.TextField(db_index=True, unique=True)),
                ('created_at', django_pg.models.fields.datetime_.DateTimeField(auto_now_add=True)),
                ('modified_at', django_pg.models.fields.datetime_.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='check',
            name='project',
            field=models.ForeignKey(related_name='checks', null=True, blank=True, to='checks.Project'),
        ),
    ]

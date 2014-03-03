# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Check'
        db.create_table('checks_check', (
            ('id', self.gf('django_pg.models.fields.uuid.UUIDField')(primary_key=True, auto_add='uuid:uuid4')),
            ('unblocked', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('created_at', self.gf('django_pg.models.fields.datetime_.DateTimeField')(default=datetime.datetime.now)),
            ('started_at', self.gf('django_pg.models.fields.datetime_.DateTimeField')(blank=True, null=True)),
            ('finished_at', self.gf('django_pg.models.fields.datetime_.DateTimeField')(blank=True, null=True)),
            ('requirements', self.gf('django_pg.models.fields.array.ArrayField')(of=('django.db.models.fields.TextField', [], {}))),
            ('projects', self.gf('django_pg.models.fields.array.ArrayField')(of=('django.db.models.fields.CharField', [], {'max_length': '100'}))),
            ('blockers', self.gf('django_pg.models.fields.json.JSONField')(default=None)),
        ))
        db.send_create_signal('checks', ['Check'])


    def backwards(self, orm):
        # Deleting model 'Check'
        db.delete_table('checks_check')


    models = {
        'checks.check': {
            'Meta': {'object_name': 'Check'},
            'blockers': ('django_pg.models.fields.json.JSONField', [], {'default': 'None'}),
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'primary_key': 'True', 'auto_add': "'uuid:uuid4'"}),
            'projects': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.CharField', [], {'max_length': '100'})}),
            'requirements': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.TextField', [], {})}),
            'started_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'unblocked': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['checks']
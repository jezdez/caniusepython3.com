# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Check.projects'
        db.alter_column('checks_check', 'projects', self.gf('django_pg.models.fields.array.ArrayField')(of=('django.db.models.fields.CharField', [], {'max_length': '255'})))

    def backwards(self, orm):

        # Changing field 'Check.projects'
        db.alter_column('checks_check', 'projects', self.gf('django_pg.models.fields.array.ArrayField')(of=('django.db.models.fields.CharField', [], {'max_length': '100'})))

    models = {
        'checks.check': {
            'Meta': {'object_name': 'Check'},
            'blockers': ('django_pg.models.fields.json.JSONField', [], {'default': 'None'}),
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'auto_add': "'uuid:uuid4'", 'primary_key': 'True'}),
            'projects': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.CharField', [], {'max_length': '255'})}),
            'requirements': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.TextField', [], {})}),
            'started_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unblocked': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['checks']
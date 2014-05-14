# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Check.project'
        db.add_column('checks_check', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='checks', null=True, blank=True, to=orm['checks.Project']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Check.project'
        db.delete_column('checks_check', 'project_id')


    models = {
        'checks.check': {
            'Meta': {'object_name': 'Check'},
            'blockers': ('django_pg.models.fields.json.JSONField', [], {'default': 'None'}),
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'primary_key': 'True', 'auto_add': "'uuid:uuid4'"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checks'", 'null': 'True', 'blank': 'True', 'to': "orm['checks.Project']"}),
            'projects': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.CharField', [], {'max_length': '255'})}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'requirements': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.TextField', [], {})}),
            'runs': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'started_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unblocked': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'checks.project': {
            'Meta': {'object_name': 'Project'},
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'primary_key': 'True', 'auto_add': "'uuid:uuid4'"}),
            'modified_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'unique': 'True'})
        }
    }

    complete_apps = ['checks']
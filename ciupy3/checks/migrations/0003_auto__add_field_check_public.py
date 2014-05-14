# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Check.public'
        db.add_column('checks_check', 'public',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Check.public'
        db.delete_column('checks_check', 'public')

    models = {
        'checks.check': {
            'Meta': {'object_name': 'Check'},
            'blockers': ('django_pg.models.fields.json.JSONField', [], {'default': 'None'}),
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'auto_add': "'uuid:uuid4'", 'primary_key': 'True'}),
            'projects': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.CharField', [], {'max_length': '255'})}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'requirements': ('django_pg.models.fields.array.ArrayField', [], {'of': ('django.db.models.fields.TextField', [], {})}),
            'started_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unblocked': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['checks']

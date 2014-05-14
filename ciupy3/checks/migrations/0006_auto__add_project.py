# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('checks_project', (
            ('id', self.gf('django_pg.models.fields.uuid.UUIDField')(auto_add='uuid:uuid4', primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True, db_index=True)),
            ('created_at', self.gf('django_pg.models.fields.datetime_.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django_pg.models.fields.datetime_.DateTimeField')(auto_now=True, blank=True)),
            ('last_check', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, blank=True, null=True, to=orm['checks.Check'])),
        ))
        db.send_create_signal('checks', ['Project'])

    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('checks_project')

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
            'runs': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'started_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unblocked': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'checks.project': {
            'Meta': {'object_name': 'Project'},
            'created_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django_pg.models.fields.uuid.UUIDField', [], {'auto_add': "'uuid:uuid4'", 'primary_key': 'True'}),
            'last_check': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['checks.Check']"}),
            'modified_at': ('django_pg.models.fields.datetime_.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['checks']

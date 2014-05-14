# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):
    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for check in orm['checks.Check'].objects.all():
            check.runs = 1
            check.save()

    def backwards(self, orm):
        "Write your backwards methods here."

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
        }
    }

    complete_apps = ['checks']
    symmetrical = True

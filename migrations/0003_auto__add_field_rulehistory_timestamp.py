# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RuleHistory.timestamp'
        db.add_column('bhp_bucket_rulehistory', 'timestamp', self.gf('django.db.models.fields.CharField')(default='000000', max_length=25), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RuleHistory.timestamp'
        db.delete_column('bhp_bucket_rulehistory', 'timestamp')


    models = {
        'bhp_bucket.rulehistory': {
            'Meta': {'ordering': "['created']", 'object_name': 'RuleHistory'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_bucket']

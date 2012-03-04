# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'RuleHistory.timestamp'
        db.alter_column('bhp_bucket_rulehistory', 'timestamp', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Adding index on 'RuleHistory', fields ['timestamp']
        db.create_index('bhp_bucket_rulehistory', ['timestamp'])


    def backwards(self, orm):
        
        # Removing index on 'RuleHistory', fields ['timestamp']
        db.delete_index('bhp_bucket_rulehistory', ['timestamp'])

        # User chose to not deal with backwards NULL issues for 'RuleHistory.timestamp'
        raise RuntimeError("Cannot reverse this migration. 'RuleHistory.timestamp' and its values cannot be restored.")


    models = {
        'bhp_bucket.rulehistory': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'RuleHistory'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rule': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_bucket']

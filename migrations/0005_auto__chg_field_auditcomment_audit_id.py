# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AuditComment.audit_id'
        db.alter_column('audit_trail_auditcomment', 'audit_id', self.gf('django.db.models.fields.CharField')(max_length=36))


    def backwards(self, orm):
        
        # Changing field 'AuditComment.audit_id'
        db.alter_column('audit_trail_auditcomment', 'audit_id', self.gf('django.db.models.fields.IntegerField')())


    models = {
        'audit_trail.auditcomment': {
            'Meta': {'ordering': "['audit_id', 'created']", 'object_name': 'AuditComment'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'audit_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'audit_comment': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'audit_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'blank': 'True'}),
            'audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['audit_trail']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'AuditComment.subject_identifier'
        db.delete_column('audit_trail_auditcomment', 'subject_identifier')

        # Adding field 'AuditComment.audit_subject_identifier'
        db.add_column('audit_trail_auditcomment', 'audit_subject_identifier', self.gf('django.db.models.fields.CharField')(default=0, max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'AuditComment.subject_identifier'
        raise RuntimeError("Cannot reverse this migration. 'AuditComment.subject_identifier' and its values cannot be restored.")

        # Deleting field 'AuditComment.audit_subject_identifier'
        db.delete_column('audit_trail_auditcomment', 'audit_subject_identifier')


    models = {
        'audit_trail.auditcomment': {
            'Meta': {'object_name': 'AuditComment'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'audit_comment': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'audit_id': ('django.db.models.fields.IntegerField', [], {}),
            'audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['audit_trail']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Link.app_label'
        db.add_column('bhp_subject_summary_link', 'app_label', self.gf('django.db.models.fields.CharField')(default='mpepu_infant', max_length=25), keep_default=False)

        # Adding field 'Link.ajax_method'
        db.add_column('bhp_subject_summary_link', 'ajax_method', self.gf('django.db.models.fields.CharField')(default='view_summary', max_length=25), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Link.app_label'
        db.delete_column('bhp_subject_summary_link', 'app_label')

        # Deleting field 'Link.ajax_method'
        db.delete_column('bhp_subject_summary_link', 'ajax_method')


    models = {
        'bhp_subject_summary.link': {
            'Meta': {'object_name': 'Link'},
            'ajax_method': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dashboard_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_subject_summary']

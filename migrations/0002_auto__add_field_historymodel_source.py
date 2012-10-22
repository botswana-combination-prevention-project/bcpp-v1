# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HistoryModel.source'
        db.add_column('bhp_lab_tracker_historymodel', 'source',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HistoryModel.source'
        db.delete_column('bhp_lab_tracker_historymodel', 'source')


    models = {
        'bhp_lab_tracker.historymodel': {
            'Meta': {'object_name': 'HistoryModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['bhp_lab_tracker']
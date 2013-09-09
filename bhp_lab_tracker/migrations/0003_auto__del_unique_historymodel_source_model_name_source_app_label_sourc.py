# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'HistoryModel', fields ['source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier']
        db.delete_unique('bhp_lab_tracker_historymodel', ['source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier'])

        # Adding unique constraint on 'HistoryModel', fields ['subject_type', 'source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier']
        db.create_unique('bhp_lab_tracker_historymodel', ['subject_type', 'source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier'])


    def backwards(self, orm):
        # Removing unique constraint on 'HistoryModel', fields ['subject_type', 'source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier']
        db.delete_unique('bhp_lab_tracker_historymodel', ['subject_type', 'source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier'])

        # Adding unique constraint on 'HistoryModel', fields ['source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier']
        db.create_unique('bhp_lab_tracker_historymodel', ['source_model_name', 'source_app_label', 'source_identifier', 'group_name', 'test_code', 'value_datetime', 'subject_identifier'])


    models = {
        'bhp_lab_tracker.defaultvaluelog': {
            'Meta': {'object_name': 'DefaultValueLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'bhp_lab_tracker.historymodel': {
            'Meta': {'unique_together': "(('source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'subject_type', 'value_datetime'),)", 'object_name': 'HistoryModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'history_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'source_app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'source_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'source_model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bhp_lab_tracker.historymodelerror': {
            'Meta': {'object_name': 'HistoryModelError'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'history_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'source_app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'source_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'source_model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bhp_lab_tracker.testresultmodel': {
            'Meta': {'object_name': 'TestResultModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'result_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_lab_tracker']
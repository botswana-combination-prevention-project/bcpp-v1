# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HistoryModel'
        db.create_table('bhp_lab_tracker_historymodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('test_code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('source_model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('source_app_label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('source_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('history_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('bhp_lab_tracker', ['HistoryModel'])

        # Adding unique constraint on 'HistoryModel', fields ['source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime']
        db.create_unique('bhp_lab_tracker_historymodel', ['source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime'])

        # Adding model 'HistoryModelError'
        db.create_table('bhp_lab_tracker_historymodelerror', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('test_code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('source_model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('source_app_label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('source_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('history_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('error_message', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('bhp_lab_tracker', ['HistoryModelError'])

        # Adding model 'DefaultValueLog'
        db.create_table('bhp_lab_tracker_defaultvaluelog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('error_message', self.gf('django.db.models.fields.TextField')(max_length=500, null=True)),
        ))
        db.send_create_signal('bhp_lab_tracker', ['DefaultValueLog'])

        # Adding model 'TestResultModel'
        db.create_table('bhp_lab_tracker_testresultmodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('result_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('bhp_lab_tracker', ['TestResultModel'])


    def backwards(self, orm):
        # Removing unique constraint on 'HistoryModel', fields ['source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime']
        db.delete_unique('bhp_lab_tracker_historymodel', ['source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime'])

        # Deleting model 'HistoryModel'
        db.delete_table('bhp_lab_tracker_historymodel')

        # Deleting model 'HistoryModelError'
        db.delete_table('bhp_lab_tracker_historymodelerror')

        # Deleting model 'DefaultValueLog'
        db.delete_table('bhp_lab_tracker_defaultvaluelog')

        # Deleting model 'TestResultModel'
        db.delete_table('bhp_lab_tracker_testresultmodel')


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
            'Meta': {'unique_together': "(('source_model_name', 'source_app_label', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime'),)", 'object_name': 'HistoryModel'},
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
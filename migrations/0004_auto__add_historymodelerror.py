# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HistoryModelError'
        db.create_table('bhp_lab_tracker_historymodelerror', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('test_code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('source_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('history_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('error_message', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('bhp_lab_tracker', ['HistoryModelError'])


    def backwards(self, orm):
        # Deleting model 'HistoryModelError'
        db.delete_table('bhp_lab_tracker_historymodelerror')


    models = {
        'bhp_lab_tracker.historymodel': {
            'Meta': {'object_name': 'HistoryModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'history_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'source_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
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
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'source_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value_datetime': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['bhp_lab_tracker']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DmisImportHistory.protocol'
        db.delete_column('lab_import_dmis_dmisimporthistory', 'protocol')

        # Deleting field 'DmisImportHistory.subject_identifier'
        db.delete_column('lab_import_dmis_dmisimporthistory', 'subject_identifier')

        # Adding field 'DmisImportHistory.lock_name'
        db.add_column('lab_import_dmis_dmisimporthistory', 'lock_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Changing field 'DmisImportHistory.start_datetime'
        db.alter_column('lab_import_dmis_dmisimporthistory', 'start_datetime', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Adding field 'DmisImportHistory.protocol'
        db.add_column('lab_import_dmis_dmisimporthistory', 'protocol',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True),
                      keep_default=False)

        # Adding field 'DmisImportHistory.subject_identifier'
        db.add_column('lab_import_dmis_dmisimporthistory', 'subject_identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True),
                      keep_default=False)

        # Deleting field 'DmisImportHistory.lock_name'
        db.delete_column('lab_import_dmis_dmisimporthistory', 'lock_name')

        # Changing field 'DmisImportHistory.start_datetime'
        db.alter_column('lab_import_dmis_dmisimporthistory', 'start_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))

    models = {
        'lab_import_dmis.dmisimporthistory': {
            'Meta': {'object_name': 'DmisImportHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lock_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 4, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_import_dmis.dmislock': {
            'Meta': {'object_name': 'DmisLock'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lock_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_import_dmis']
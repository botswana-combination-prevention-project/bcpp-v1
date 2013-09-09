# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'AliquotMedium', fields ['hostname_created']
        db.create_index('bhp_lab_core_aliquotmedium', ['hostname_created'])

        # Adding index on 'AliquotMedium', fields ['hostname_modified']
        db.create_index('bhp_lab_core_aliquotmedium', ['hostname_modified'])

        # Adding index on 'AliquotCondition', fields ['hostname_created']
        db.create_index('bhp_lab_core_aliquotcondition', ['hostname_created'])

        # Adding index on 'AliquotCondition', fields ['hostname_modified']
        db.create_index('bhp_lab_core_aliquotcondition', ['hostname_modified'])

        # Adding index on 'AliquotType', fields ['hostname_created']
        db.create_index('bhp_lab_core_aliquottype', ['hostname_created'])

        # Adding index on 'AliquotType', fields ['hostname_modified']
        db.create_index('bhp_lab_core_aliquottype', ['hostname_modified'])


    def backwards(self, orm):
        # Removing index on 'AliquotType', fields ['hostname_modified']
        db.delete_index('bhp_lab_core_aliquottype', ['hostname_modified'])

        # Removing index on 'AliquotType', fields ['hostname_created']
        db.delete_index('bhp_lab_core_aliquottype', ['hostname_created'])

        # Removing index on 'AliquotCondition', fields ['hostname_modified']
        db.delete_index('bhp_lab_core_aliquotcondition', ['hostname_modified'])

        # Removing index on 'AliquotCondition', fields ['hostname_created']
        db.delete_index('bhp_lab_core_aliquotcondition', ['hostname_created'])

        # Removing index on 'AliquotMedium', fields ['hostname_modified']
        db.delete_index('bhp_lab_core_aliquotmedium', ['hostname_modified'])

        # Removing index on 'AliquotMedium', fields ['hostname_created']
        db.delete_index('bhp_lab_core_aliquotmedium', ['hostname_created'])


    models = {
        'lab_aliquot_list.aliquotcondition': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'AliquotCondition', 'db_table': "'bhp_lab_core_aliquotcondition'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'lab_aliquot_list.aliquotmedium': {
            'Meta': {'ordering': "['name']", 'object_name': 'AliquotMedium', 'db_table': "'bhp_lab_core_aliquotmedium'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'lab_aliquot_list.aliquottype': {
            'Meta': {'ordering': "['name']", 'object_name': 'AliquotType', 'db_table': "'bhp_lab_core_aliquottype'"},
            'alpha_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dmis_reference': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_aliquot_list']
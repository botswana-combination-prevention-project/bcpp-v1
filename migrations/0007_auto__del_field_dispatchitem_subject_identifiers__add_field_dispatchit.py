# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Dispatch', fields ['user_modified']
        db.create_index('bhp_dispatch_dispatch', ['user_modified'])

        # Adding index on 'Dispatch', fields ['user_created']
        db.create_index('bhp_dispatch_dispatch', ['user_created'])

        # Deleting field 'DispatchItem.subject_identifiers'
        db.rename_column('bhp_dispatch_dispatchitem', 'subject_identifiers', 'registered_subjects')

        # Adding field 'DispatchItem.item_app_name'
        db.add_column('bhp_dispatch_dispatchitem', 'item_app_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.item_model_name'
        db.add_column('bhp_dispatch_dispatchitem', 'item_model_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.item_identifier_attrname'
        db.add_column('bhp_dispatch_dispatchitem', 'item_identifier_attrname',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.dispatched_using'
        db.add_column('bhp_dispatch_dispatchitem', 'dispatched_using',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding index on 'DispatchItem', fields ['user_modified']
        db.create_index('bhp_dispatch_dispatchitem', ['user_modified'])

        # Adding index on 'DispatchItem', fields ['user_created']
        db.create_index('bhp_dispatch_dispatchitem', ['user_created'])

        # Adding unique constraint on 'DispatchItem', fields ['is_dispatched', 'item_identifier']
        db.create_unique('bhp_dispatch_dispatchitem', ['is_dispatched', 'item_identifier'])

        # Adding index on 'PrepareHistory', fields ['user_modified']
        db.create_index('bhp_dispatch_preparehistory', ['user_modified'])

        # Adding index on 'PrepareHistory', fields ['user_created']
        db.create_index('bhp_dispatch_preparehistory', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'PrepareHistory', fields ['user_created']
        db.delete_index('bhp_dispatch_preparehistory', ['user_created'])

        # Removing index on 'PrepareHistory', fields ['user_modified']
        db.delete_index('bhp_dispatch_preparehistory', ['user_modified'])

        # Removing unique constraint on 'DispatchItem', fields ['is_dispatched', 'item_identifier']
        db.delete_unique('bhp_dispatch_dispatchitem', ['is_dispatched', 'item_identifier'])

        # Removing index on 'DispatchItem', fields ['user_created']
        db.delete_index('bhp_dispatch_dispatchitem', ['user_created'])

        # Removing index on 'DispatchItem', fields ['user_modified']
        db.delete_index('bhp_dispatch_dispatchitem', ['user_modified'])

        # Removing index on 'Dispatch', fields ['user_created']
        db.delete_index('bhp_dispatch_dispatch', ['user_created'])

        # Removing index on 'Dispatch', fields ['user_modified']
        db.delete_index('bhp_dispatch_dispatch', ['user_modified'])

        # Adding field 'DispatchItem.subject_identifiers'
        db.add_column('bhp_dispatch_dispatchitem', 'subject_identifiers',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'DispatchItem.item_app_name'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_app_name')

        # Deleting field 'DispatchItem.item_model_name'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_model_name')

        # Deleting field 'DispatchItem.item_identifier_attrname'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_identifier_attrname')

        # Deleting field 'DispatchItem.dispatched_using'
        db.delete_column('bhp_dispatch_dispatchitem', 'dispatched_using')

        # Deleting field 'DispatchItem.registered_subjects'
        db.delete_column('bhp_dispatch_dispatchitem', 'registered_subjects')


    models = {
        'bhp_dispatch.dispatch': {
            'Meta': {'object_name': 'Dispatch'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatch_items': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'return_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_dispatch.dispatchitem': {
            'Meta': {'unique_together': "(('item_identifier', 'is_dispatched'),)", 'object_name': 'DispatchItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_dispatch.Dispatch']"}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatched_using': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_app_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'item_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'registered_subjects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'return_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_dispatch.preparehistory': {
            'Meta': {'object_name': 'PrepareHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prepare_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 20, 0, 0)'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.producer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Producer'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'settings_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_dispatch']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DispatchContainer.container_app_name'
        db.add_column('bhp_dispatch_dispatchcontainer', 'container_app_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchContainer.container_model_name'
        db.add_column('bhp_dispatch_dispatchcontainer', 'container_model_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchContainer.container_identifier_attrname'
        db.add_column('bhp_dispatch_dispatchcontainer', 'container_identifier_attrname',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchContainer.container_identifier'
        db.add_column('bhp_dispatch_dispatchcontainer', 'container_identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchContainer.container_pk'
        db.add_column('bhp_dispatch_dispatchcontainer', 'container_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'DispatchContainer.dispatched_using'
        db.add_column('bhp_dispatch_dispatchcontainer', 'dispatched_using',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Deleting field 'DispatchItem.item_app_name'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_app_name')

        # Deleting field 'DispatchItem.item_model_name'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_model_name')

        # Deleting field 'DispatchItem.dispatched_using'
        db.delete_column('bhp_dispatch_dispatchitem', 'dispatched_using')

        # Deleting field 'DispatchItem.item_identifier_attrname'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_identifier_attrname')


    def backwards(self, orm):
        # Deleting field 'DispatchContainer.container_app_name'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'container_app_name')

        # Deleting field 'DispatchContainer.container_model_name'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'container_model_name')

        # Deleting field 'DispatchContainer.container_identifier_attrname'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'container_identifier_attrname')

        # Deleting field 'DispatchContainer.container_identifier'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'container_identifier')

        # Deleting field 'DispatchContainer.container_pk'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'container_pk')

        # Deleting field 'DispatchContainer.dispatched_using'
        db.delete_column('bhp_dispatch_dispatchcontainer', 'dispatched_using')

        # Adding field 'DispatchItem.item_app_name'
        db.add_column('bhp_dispatch_dispatchitem', 'item_app_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.item_model_name'
        db.add_column('bhp_dispatch_dispatchitem', 'item_model_name',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.dispatched_using'
        db.add_column('bhp_dispatch_dispatchitem', 'dispatched_using',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)

        # Adding field 'DispatchItem.item_identifier_attrname'
        db.add_column('bhp_dispatch_dispatchitem', 'item_identifier_attrname',
                      self.gf('django.db.models.fields.CharField')(max_length=35, null=True),
                      keep_default=False)


    models = {
        'bhp_dispatch.dispatchcontainer': {
            'Meta': {'object_name': 'DispatchContainer'},
            'container_app_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'container_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'container_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'container_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'container_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 21, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatch_items': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'dispatched_using': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
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
            'dispatch_container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_dispatch.DispatchContainer']"}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 21, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
            'prepare_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 21, 0, 0)'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_dispatch.testitem': {
            'Meta': {'object_name': 'TestItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_dispatch.testitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestItemAudit', 'db_table': "'bhp_dispatch_testitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.producer': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('settings_key', 'is_active'),)", 'object_name': 'Producer'},
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
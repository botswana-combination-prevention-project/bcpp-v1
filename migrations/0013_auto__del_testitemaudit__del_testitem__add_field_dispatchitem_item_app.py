# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestItemAudit'
        db.delete_table('bhp_dispatch_testitem_audit')

        # Deleting model 'TestItem'
        db.delete_table('bhp_dispatch_testitem')

        # Adding field 'DispatchItem.item_app_label'
        db.add_column('bhp_dispatch_dispatchitem', 'item_app_label',
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

        # Adding field 'DispatchItem.item_pk'
        db.add_column('bhp_dispatch_dispatchitem', 'item_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


        # Changing field 'DispatchItem.item_identifier'
        db.alter_column('bhp_dispatch_dispatchitem', 'item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True))

    def backwards(self, orm):
        # Adding model 'TestItemAudit'
        db.create_table('bhp_dispatch_testitem_audit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('bhp_dispatch', ['TestItemAudit'])

        # Adding model 'TestItem'
        db.create_table('bhp_dispatch_testitem', (
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_dispatch', ['TestItem'])

        # Deleting field 'DispatchItem.item_app_label'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_app_label')

        # Deleting field 'DispatchItem.item_model_name'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_model_name')

        # Deleting field 'DispatchItem.item_identifier_attrname'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_identifier_attrname')

        # Deleting field 'DispatchItem.item_pk'
        db.delete_column('bhp_dispatch_dispatchitem', 'item_pk')


        # User chose to not deal with backwards NULL issues for 'DispatchItem.item_identifier'
        raise RuntimeError("Cannot reverse this migration. 'DispatchItem.item_identifier' and its values cannot be restored.")

    models = {
        'bhp_dispatch.dispatchcontainer': {
            'Meta': {'object_name': 'DispatchContainer'},
            'container_app_label': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
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
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item_app_label': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'item_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
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
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
         
        db.create_table('bhp_sync_middlemantransaction', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(default='', max_length=36, primary_key=True)),
            ('tx_name', self.gf('django.db.models.fields.CharField')(default=2, max_length=64, db_index=True)),
            ('tx_pk', self.gf('django.db.models.fields.CharField')(default=2, max_length=36)),
            ('tx', self.gf('django.db.models.fields.TextField')(default=2)),
            ('producer', self.gf('django.db.models.fields.CharField')(default='one.local-bhp066', max_length=50, db_index=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('is_consumed_middleman', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_consumed_server', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('consumed_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('consumer', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=25, null=True, blank=True)),
            ('batch_seq', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('batch_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
         ))
        db.send_create_signal('bhp_sync', ['MiddleManTransaction'])
        
        db.add_column('bhp_sync_middlemantransaction', 'is_error', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True), keep_default=False)

        # Adding field 'OutgoingTransaction.is_error'
        db.add_column('bhp_sync_middlemantransaction', 'is_ignored', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True), keep_default=False)

        # Adding field 'Transaction.is_error'
        db.add_column('bhp_sync_middlemantransaction', 'error', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True), keep_default=False)
        
    def backwards(self, orm):
        pass
        # Adding field 'MiddleManTransaction.outgoingtransaction_ptr'
#         db.add_column('bhp_sync_middlemantransaction', 'outgoingtransaction_ptr',
#                       self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['bhp_sync.OutgoingTransaction'], unique=True, primary_key=True),
#                       keep_default=False)
# 
#         # Deleting field 'MiddleManTransaction.created'
#         db.delete_column('bhp_sync_middlemantransaction', 'created')
# 
#         # Deleting field 'MiddleManTransaction.modified'
#         db.delete_column('bhp_sync_middlemantransaction', 'modified')
# 
#         # Deleting field 'MiddleManTransaction.user_created'
#         db.delete_column('bhp_sync_middlemantransaction', 'user_created')
# 
#         # Deleting field 'MiddleManTransaction.user_modified'
#         db.delete_column('bhp_sync_middlemantransaction', 'user_modified')
# 
#         # Deleting field 'MiddleManTransaction.hostname_created'
#         db.delete_column('bhp_sync_middlemantransaction', 'hostname_created')
# 
#         # Deleting field 'MiddleManTransaction.hostname_modified'
#         db.delete_column('bhp_sync_middlemantransaction', 'hostname_modified')
# 
#         # Deleting field 'MiddleManTransaction.id'
#         db.delete_column('bhp_sync_middlemantransaction', 'id')
# 
#         # Deleting field 'MiddleManTransaction.tx'
#         db.delete_column('bhp_sync_middlemantransaction', 'tx')
# 
#         # Deleting field 'MiddleManTransaction.tx_name'
#         db.delete_column('bhp_sync_middlemantransaction', 'tx_name')
# 
#         # Deleting field 'MiddleManTransaction.tx_pk'
#         db.delete_column('bhp_sync_middlemantransaction', 'tx_pk')
# 
#         # Deleting field 'MiddleManTransaction.producer'
#         db.delete_column('bhp_sync_middlemantransaction', 'producer')
# 
#         # Deleting field 'MiddleManTransaction.action'
#         db.delete_column('bhp_sync_middlemantransaction', 'action')
# 
#         # Deleting field 'MiddleManTransaction.timestamp'
#         db.delete_column('bhp_sync_middlemantransaction', 'timestamp')
# 
#         # Deleting field 'MiddleManTransaction.consumed_datetime'
#         db.delete_column('bhp_sync_middlemantransaction', 'consumed_datetime')
# 
#         # Deleting field 'MiddleManTransaction.consumer'
#         db.delete_column('bhp_sync_middlemantransaction', 'consumer')
# 
#         # Deleting field 'MiddleManTransaction.is_ignored'
#         db.delete_column('bhp_sync_middlemantransaction', 'is_ignored')
# 
#         # Deleting field 'MiddleManTransaction.is_error'
#         db.delete_column('bhp_sync_middlemantransaction', 'is_error')
# 
#         # Deleting field 'MiddleManTransaction.error'
#         db.delete_column('bhp_sync_middlemantransaction', 'error')
# 
#         # Deleting field 'MiddleManTransaction.batch_seq'
#         db.delete_column('bhp_sync_middlemantransaction', 'batch_seq')
# 
#         # Deleting field 'MiddleManTransaction.batch_id'
#         db.delete_column('bhp_sync_middlemantransaction', 'batch_id')
# 
#         # Deleting field 'MiddleManTransaction.is_consumed_middleman'
#         db.delete_column('bhp_sync_middlemantransaction', 'is_consumed_middleman')
# 
#         # Deleting field 'MiddleManTransaction.is_consumed_server'
#         db.delete_column('bhp_sync_middlemantransaction', 'is_consumed_server')


    models = {
        'bhp_sync.incomingtransaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'IncomingTransaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_self': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'one.local-bhp066'", 'max_length': '50', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.middlemantransaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'MiddleManTransaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed_middleman': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_consumed_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'one.local-bhp066'", 'max_length': '50', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.outgoingtransaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'OutgoingTransaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed_middleman': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_consumed_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'one.local-bhp066'", 'max_length': '50', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.producer': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('settings_key', 'is_active'),)", 'object_name': 'Producer'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'settings_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'request_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 31, 0, 0)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'complete'", 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.syncimporthistorymodel': {
            'Meta': {'object_name': 'SyncImportHistoryModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lock_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 31, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.synclockmodel': {
            'Meta': {'object_name': 'SyncLockModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lock_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.testitem': {
            'Meta': {'object_name': 'TestItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.testitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestItemAudit', 'db_table': "'bhp_sync_testitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_sync.transaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Transaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'one.local-bhp066'", 'max_length': '50', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_sync']
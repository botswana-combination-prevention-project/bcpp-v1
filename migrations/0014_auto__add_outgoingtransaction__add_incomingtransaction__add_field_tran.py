# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OutgoingTransaction'
        db.create_table('bhp_sync_outgoingtransaction', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('tx_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('tx_pk', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('tx', self.gf('django.db.models.fields.TextField')()),
            ('producer', self.gf('django.db.models.fields.CharField')(default='mac.local-bhp062', max_length=25, db_index=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('is_consumed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumed_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('consumer', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('batch_seq', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('batch_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('bhp_sync', ['OutgoingTransaction'])

        # Adding model 'IncomingTransaction'
        db.create_table('bhp_sync_incomingtransaction', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('tx_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('tx_pk', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('tx', self.gf('django.db.models.fields.TextField')()),
            ('producer', self.gf('django.db.models.fields.CharField')(default='mac.local-bhp062', max_length=25, db_index=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('is_consumed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consumed_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('consumer', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('batch_seq', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('batch_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('bhp_sync', ['IncomingTransaction'])

        # Adding field 'Transaction.batch_seq'
        db.add_column('bhp_sync_transaction', 'batch_seq', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Transaction.batch_id'
        db.add_column('bhp_sync_transaction', 'batch_id', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'OutgoingTransaction'
        db.delete_table('bhp_sync_outgoingtransaction')

        # Deleting model 'IncomingTransaction'
        db.delete_table('bhp_sync_incomingtransaction')

        # Deleting field 'Transaction.batch_seq'
        db.delete_column('bhp_sync_transaction', 'batch_seq')

        # Deleting field 'Transaction.batch_id'
        db.delete_column('bhp_sync_transaction', 'batch_id')


    models = {
        'bhp_sync.incomingtransaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'IncomingTransaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_sync.outgoingtransaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'OutgoingTransaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_sync.producer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Producer'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_sync.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'request_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 5, 15, 10, 51, 559128)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'complete'", 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_sync.transaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Transaction'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'batch_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'batch_seq': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'consumed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'consumer': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_sync']

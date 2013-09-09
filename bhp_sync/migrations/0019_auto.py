# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Producer', fields ['hostname_created']
        db.create_index('bhp_sync_producer', ['hostname_created'])

        # Adding index on 'Producer', fields ['hostname_modified']
        db.create_index('bhp_sync_producer', ['hostname_modified'])

        # Adding index on 'IncomingTransaction', fields ['tx_name']
        db.create_index('bhp_sync_incomingtransaction', ['tx_name'])

        # Adding index on 'IncomingTransaction', fields ['hostname_created']
        db.create_index('bhp_sync_incomingtransaction', ['hostname_created'])

        # Adding index on 'IncomingTransaction', fields ['is_error']
        db.create_index('bhp_sync_incomingtransaction', ['is_error'])

        # Adding index on 'IncomingTransaction', fields ['is_consumed']
        db.create_index('bhp_sync_incomingtransaction', ['is_consumed'])

        # Adding index on 'IncomingTransaction', fields ['hostname_modified']
        db.create_index('bhp_sync_incomingtransaction', ['hostname_modified'])

        # Adding index on 'OutgoingTransaction', fields ['tx_name']
        db.create_index('bhp_sync_outgoingtransaction', ['tx_name'])

        # Adding index on 'OutgoingTransaction', fields ['hostname_created']
        db.create_index('bhp_sync_outgoingtransaction', ['hostname_created'])

        # Adding index on 'OutgoingTransaction', fields ['is_error']
        db.create_index('bhp_sync_outgoingtransaction', ['is_error'])

        # Adding index on 'OutgoingTransaction', fields ['is_consumed']
        db.create_index('bhp_sync_outgoingtransaction', ['is_consumed'])

        # Adding index on 'OutgoingTransaction', fields ['hostname_modified']
        db.create_index('bhp_sync_outgoingtransaction', ['hostname_modified'])

        # Adding index on 'RequestLog', fields ['hostname_created']
        db.create_index('bhp_sync_requestlog', ['hostname_created'])

        # Adding index on 'RequestLog', fields ['hostname_modified']
        db.create_index('bhp_sync_requestlog', ['hostname_modified'])

        # Adding index on 'Transaction', fields ['tx_name']
        db.create_index('bhp_sync_transaction', ['tx_name'])

        # Adding index on 'Transaction', fields ['hostname_created']
        db.create_index('bhp_sync_transaction', ['hostname_created'])

        # Adding index on 'Transaction', fields ['is_error']
        db.create_index('bhp_sync_transaction', ['is_error'])

        # Adding index on 'Transaction', fields ['is_consumed']
        db.create_index('bhp_sync_transaction', ['is_consumed'])

        # Adding index on 'Transaction', fields ['hostname_modified']
        db.create_index('bhp_sync_transaction', ['hostname_modified'])


    def backwards(self, orm):
        
        # Removing index on 'Transaction', fields ['hostname_modified']
        db.delete_index('bhp_sync_transaction', ['hostname_modified'])

        # Removing index on 'Transaction', fields ['is_consumed']
        db.delete_index('bhp_sync_transaction', ['is_consumed'])

        # Removing index on 'Transaction', fields ['is_error']
        db.delete_index('bhp_sync_transaction', ['is_error'])

        # Removing index on 'Transaction', fields ['hostname_created']
        db.delete_index('bhp_sync_transaction', ['hostname_created'])

        # Removing index on 'Transaction', fields ['tx_name']
        db.delete_index('bhp_sync_transaction', ['tx_name'])

        # Removing index on 'RequestLog', fields ['hostname_modified']
        db.delete_index('bhp_sync_requestlog', ['hostname_modified'])

        # Removing index on 'RequestLog', fields ['hostname_created']
        db.delete_index('bhp_sync_requestlog', ['hostname_created'])

        # Removing index on 'OutgoingTransaction', fields ['hostname_modified']
        db.delete_index('bhp_sync_outgoingtransaction', ['hostname_modified'])

        # Removing index on 'OutgoingTransaction', fields ['is_consumed']
        db.delete_index('bhp_sync_outgoingtransaction', ['is_consumed'])

        # Removing index on 'OutgoingTransaction', fields ['is_error']
        db.delete_index('bhp_sync_outgoingtransaction', ['is_error'])

        # Removing index on 'OutgoingTransaction', fields ['hostname_created']
        db.delete_index('bhp_sync_outgoingtransaction', ['hostname_created'])

        # Removing index on 'OutgoingTransaction', fields ['tx_name']
        db.delete_index('bhp_sync_outgoingtransaction', ['tx_name'])

        # Removing index on 'IncomingTransaction', fields ['hostname_modified']
        db.delete_index('bhp_sync_incomingtransaction', ['hostname_modified'])

        # Removing index on 'IncomingTransaction', fields ['is_consumed']
        db.delete_index('bhp_sync_incomingtransaction', ['is_consumed'])

        # Removing index on 'IncomingTransaction', fields ['is_error']
        db.delete_index('bhp_sync_incomingtransaction', ['is_error'])

        # Removing index on 'IncomingTransaction', fields ['hostname_created']
        db.delete_index('bhp_sync_incomingtransaction', ['hostname_created'])

        # Removing index on 'IncomingTransaction', fields ['tx_name']
        db.delete_index('bhp_sync_incomingtransaction', ['tx_name'])

        # Removing index on 'Producer', fields ['hostname_modified']
        db.delete_index('bhp_sync_producer', ['hostname_modified'])

        # Removing index on 'Producer', fields ['hostname_created']
        db.delete_index('bhp_sync_producer', ['hostname_created'])


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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'request_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 22, 13, 20, 50, 637509)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'complete'", 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_consumed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.CharField', [], {'default': "'mac.local-bhp062'", 'max_length': '25', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_sync']

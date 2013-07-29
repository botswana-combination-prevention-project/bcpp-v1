# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transaction'
        db.create_table('bhp_sync_transaction', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('tx_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('tx_pk', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('tx', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('is_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('bhp_sync', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Transaction'
        db.delete_table('bhp_sync_transaction')


    models = {
        'bhp_sync.transaction': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Transaction'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'sent_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'tx_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_sync']

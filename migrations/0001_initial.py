# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HBCDispatch'
        db.create_table('bhp_dispatch_hbcdispatch', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_sync.Producer'])),
            ('is_checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_checked_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datetime_checked_out', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('datetime_checked_in', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('checkout_items', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('bhp_dispatch', ['HBCDispatch'])

        # Adding model 'HBCDispatchItem'
        db.create_table('bhp_dispatch_hbcdispatchitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_sync.Producer'])),
            ('is_checked_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_checked_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datetime_checked_out', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('datetime_checked_in', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('hbc_dispatch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_dispatch.HBCDispatch'], null=True)),
            ('item_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bhp_dispatch', ['HBCDispatchItem'])


    def backwards(self, orm):
        # Deleting model 'HBCDispatch'
        db.delete_table('bhp_dispatch_hbcdispatch')

        # Deleting model 'HBCDispatchItem'
        db.delete_table('bhp_dispatch_hbcdispatchitem')


    models = {
        'bhp_dispatch.hbcdispatch': {
            'Meta': {'object_name': 'HBCDispatch'},
            'checkout_items': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_checked_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_checked_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_checked_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_dispatch.hbcdispatchitem': {
            'Meta': {'object_name': 'HBCDispatchItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_checked_in': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_checked_out': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hbc_dispatch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_dispatch.HBCDispatch']", 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_checked_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_sync.Producer']"}),
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
            'settings_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_dispatch']
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PackingList'
        db.create_table('lab_packing_packinglist', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='s014', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='s014', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('list_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('list_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 12, 8, 13, 46, 27, 61469))),
            ('list_comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('lab_packing', ['PackingList'])

        # Adding model 'PackingListItem'
        db.create_table('lab_packing_packinglistitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='s014', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='s014', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('packing_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_packing.PackingList'])),
            ('item_reference', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('item_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('item_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('lab_packing', ['PackingListItem'])


    def backwards(self, orm):
        
        # Deleting model 'PackingList'
        db.delete_table('lab_packing_packinglist')

        # Deleting model 'PackingListItem'
        db.delete_table('lab_packing_packinglistitem')


    models = {
        'lab_packing.packinglist': {
            'Meta': {'object_name': 'PackingList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'list_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'list_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 12, 8, 13, 46, 27, 61469)'}),
            'list_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_packing.packinglistitem': {
            'Meta': {'object_name': 'PackingListItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'item_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'item_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'item_reference': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'packing_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_packing.PackingList']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_packing']

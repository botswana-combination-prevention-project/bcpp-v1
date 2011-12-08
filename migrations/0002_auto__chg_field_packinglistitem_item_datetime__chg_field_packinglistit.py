# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'PackingListItem.item_datetime'
        db.alter_column('lab_packing_packinglistitem', 'item_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PackingListItem.item_description'
        db.alter_column('lab_packing_packinglistitem', 'item_description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'PackingListItem.item_datetime'
        raise RuntimeError("Cannot reverse this migration. 'PackingListItem.item_datetime' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PackingListItem.item_description'
        raise RuntimeError("Cannot reverse this migration. 'PackingListItem.item_description' and its values cannot be restored.")


    models = {
        'lab_packing.packinglist': {
            'Meta': {'object_name': 'PackingList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'list_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'list_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 12, 8, 14, 8, 16, 331365)'}),
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
            'item_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'item_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'item_reference': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'packing_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_packing.PackingList']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_packing']

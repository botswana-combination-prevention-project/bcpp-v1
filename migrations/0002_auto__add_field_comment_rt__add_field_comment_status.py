# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Comment.rt'
        db.add_column('bhp_data_manager_comment', 'rt',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Comment.status'
        db.add_column('bhp_data_manager_comment', 'status',
                      self.gf('django.db.models.fields.CharField')(default='Open', max_length=35),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Comment.rt'
        db.delete_column('bhp_data_manager_comment', 'rt')

        # Deleting field 'Comment.status'
        db.delete_column('bhp_data_manager_comment', 'status')


    models = {
        'bhp_data_manager.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'comment_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 14, 0, 0)'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'rt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '35'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_data_manager']
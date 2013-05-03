# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataNote'
        db.create_table('bhp_data_manager_datanote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 5, 3, 0, 0))),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('display_on_dashboard', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('rt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Open', max_length=35)),
        ))
        db.send_create_signal('bhp_data_manager', ['DataNote'])

        # Adding index on 'Comment', fields ['user_modified']
        db.create_index('bhp_data_manager_comment', ['user_modified'])

        # Adding index on 'Comment', fields ['user_created']
        db.create_index('bhp_data_manager_comment', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'Comment', fields ['user_created']
        db.delete_index('bhp_data_manager_comment', ['user_created'])

        # Removing index on 'Comment', fields ['user_modified']
        db.delete_index('bhp_data_manager_comment', ['user_modified'])

        # Deleting model 'DataNote'
        db.delete_table('bhp_data_manager_datanote')


    models = {
        'bhp_data_manager.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'comment_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 3, 0, 0)'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'rt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '35'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_data_manager.datanote': {
            'Meta': {'object_name': 'DataNote'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'comment_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 3, 0, 0)'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'rt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '35'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_data_manager']
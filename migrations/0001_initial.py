# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Related'
        db.create_table('bhp_describer_related', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('related_to_model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('related_to_field_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('bhp_model_describer', ['Related'])

        # Adding unique constraint on 'Related', fields ['app_label', 'model_name', 'field_name']
        db.create_unique('bhp_describer_related', ['app_label', 'model_name', 'field_name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Related', fields ['app_label', 'model_name', 'field_name']
        db.delete_unique('bhp_describer_related', ['app_label', 'model_name', 'field_name'])

        # Deleting model 'Related'
        db.delete_table('bhp_describer_related')


    models = {
        'bhp_model_describer.related': {
            'Meta': {'unique_together': "(['app_label', 'model_name', 'field_name'],)", 'object_name': 'Related'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'related_to_field_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'related_to_model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_model_describer']

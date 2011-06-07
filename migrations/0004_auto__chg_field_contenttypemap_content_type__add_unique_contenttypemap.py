# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ContentTypeMap.content_type'
        db.alter_column('bhp_common_contenttypemap', 'content_type_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttypes.ContentType'], unique=True))

        # Adding unique constraint on 'ContentTypeMap', fields ['content_type']
        db.create_unique('bhp_common_contenttypemap', ['content_type_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ContentTypeMap', fields ['content_type']
        db.delete_unique('bhp_common_contenttypemap', ['content_type_id'])

        # Changing field 'ContentTypeMap.content_type'
        db.alter_column('bhp_common_contenttypemap', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))


    models = {
        'bhp_common.contenttypemap': {
            'Meta': {'object_name': 'ContentTypeMap'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content_type': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttypes.ContentType']", 'unique': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bhp_common']

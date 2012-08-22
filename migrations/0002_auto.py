# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'ContentTypeMap', fields ['hostname_modified']
        db.create_index('bhp_common_contenttypemap', ['hostname_modified'])

        # Adding index on 'ContentTypeMap', fields ['name']
        db.create_index('bhp_common_contenttypemap', ['name'])

        # Adding index on 'ContentTypeMap', fields ['hostname_created']
        db.create_index('bhp_common_contenttypemap', ['hostname_created'])

        # Adding index on 'ContentTypeMap', fields ['app_label']
        db.create_index('bhp_common_contenttypemap', ['app_label'])

        # Adding index on 'ContentTypeMap', fields ['model']
        db.create_index('bhp_common_contenttypemap', ['model'])


    def backwards(self, orm):
        # Removing index on 'ContentTypeMap', fields ['model']
        db.delete_index('bhp_common_contenttypemap', ['model'])

        # Removing index on 'ContentTypeMap', fields ['app_label']
        db.delete_index('bhp_common_contenttypemap', ['app_label'])

        # Removing index on 'ContentTypeMap', fields ['hostname_created']
        db.delete_index('bhp_common_contenttypemap', ['hostname_created'])

        # Removing index on 'ContentTypeMap', fields ['name']
        db.delete_index('bhp_common_contenttypemap', ['name'])

        # Removing index on 'ContentTypeMap', fields ['hostname_modified']
        db.delete_index('bhp_common_contenttypemap', ['hostname_modified'])


    models = {
        'bhp_content_type_map.contenttypemap': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap', 'db_table': "'bhp_common_contenttypemap'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
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

    complete_apps = ['bhp_content_type_map']
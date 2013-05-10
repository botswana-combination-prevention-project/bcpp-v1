# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'PendingIdentifier', fields ['user_modified']
        db.create_index('bhp_identifier_pendingidentifier', ['user_modified'])

        # Adding index on 'PendingIdentifier', fields ['user_created']
        db.create_index('bhp_identifier_pendingidentifier', ['user_created'])

        # Adding index on 'IdentifierTracker', fields ['user_modified']
        db.create_index('bhp_identifier_identifiertracker', ['user_modified'])

        # Adding index on 'IdentifierTracker', fields ['user_created']
        db.create_index('bhp_identifier_identifiertracker', ['user_created'])

        # Adding field 'DerivedSubjectIdentifier.padding'
        db.add_column('bhp_identifier_derivedsubjectidentifier', 'padding',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding index on 'DerivedSubjectIdentifier', fields ['user_modified']
        db.create_index('bhp_identifier_derivedsubjectidentifier', ['user_modified'])

        # Adding index on 'DerivedSubjectIdentifier', fields ['user_created']
        db.create_index('bhp_identifier_derivedsubjectidentifier', ['user_created'])

        # Adding index on 'Sequence', fields ['user_modified']
        db.create_index('bhp_identifier_sequence', ['user_modified'])

        # Adding index on 'Sequence', fields ['user_created']
        db.create_index('bhp_identifier_sequence', ['user_created'])

        # Adding field 'SubjectIdentifier.is_derived'
        db.add_column('bhp_identifier_subjectidentifier', 'is_derived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding index on 'SubjectIdentifier', fields ['user_modified']
        db.create_index('bhp_identifier_subjectidentifier', ['user_modified'])

        # Adding index on 'SubjectIdentifier', fields ['user_created']
        db.create_index('bhp_identifier_subjectidentifier', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'SubjectIdentifier', fields ['user_created']
        db.delete_index('bhp_identifier_subjectidentifier', ['user_created'])

        # Removing index on 'SubjectIdentifier', fields ['user_modified']
        db.delete_index('bhp_identifier_subjectidentifier', ['user_modified'])

        # Removing index on 'Sequence', fields ['user_created']
        db.delete_index('bhp_identifier_sequence', ['user_created'])

        # Removing index on 'Sequence', fields ['user_modified']
        db.delete_index('bhp_identifier_sequence', ['user_modified'])

        # Removing index on 'DerivedSubjectIdentifier', fields ['user_created']
        db.delete_index('bhp_identifier_derivedsubjectidentifier', ['user_created'])

        # Removing index on 'DerivedSubjectIdentifier', fields ['user_modified']
        db.delete_index('bhp_identifier_derivedsubjectidentifier', ['user_modified'])

        # Removing index on 'IdentifierTracker', fields ['user_created']
        db.delete_index('bhp_identifier_identifiertracker', ['user_created'])

        # Removing index on 'IdentifierTracker', fields ['user_modified']
        db.delete_index('bhp_identifier_identifiertracker', ['user_modified'])

        # Removing index on 'PendingIdentifier', fields ['user_created']
        db.delete_index('bhp_identifier_pendingidentifier', ['user_created'])

        # Removing index on 'PendingIdentifier', fields ['user_modified']
        db.delete_index('bhp_identifier_pendingidentifier', ['user_modified'])

        # Deleting field 'DerivedSubjectIdentifier.padding'
        db.delete_column('bhp_identifier_derivedsubjectidentifier', 'padding')

        # Deleting field 'SubjectIdentifier.is_derived'
        db.delete_column('bhp_identifier_subjectidentifier', 'is_derived')


    models = {
        'bhp_identifier.derivedsubjectidentifier': {
            'Meta': {'object_name': 'DerivedSubjectIdentifier'},
            'base_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_identifier.identifiertracker': {
            'Meta': {'ordering': "['root_number', 'counter']", 'unique_together': "(['root_number', 'counter'],)", 'object_name': 'IdentifierTracker'},
            'counter': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'identifier_string': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'identifier_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'root_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_identifier.pendingidentifier': {
            'Meta': {'ordering': "['id']", 'object_name': 'PendingIdentifier'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'final_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'final_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pending_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 10, 0, 0)'}),
            'pending_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_identifier.sequence': {
            'Meta': {'ordering': "['id']", 'object_name': 'Sequence'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_identifier.subjectidentifier': {
            'Meta': {'ordering': "['-created']", 'object_name': 'SubjectIdentifier'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'is_derived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_identifier']
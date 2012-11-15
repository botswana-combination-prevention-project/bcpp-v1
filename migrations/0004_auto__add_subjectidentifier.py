# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        pass        
        # Adding model 'SubjectIdentifier'
#        db.create_table('bhp_identifier_subjectidentifier', (
#            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
#            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
#            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
#            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
#            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
#            ('subject_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
#            ('seed', self.gf('django.db.models.fields.IntegerField')(default=1000, unique=True)),
#        ))
#        db.send_create_signal('bhp_identifier', ['SubjectIdentifier'])

        # Adding index on 'IdentifierTracker', fields ['hostname_created']
#        db.create_index('bhp_identifier_identifiertracker', ['hostname_created'])

        # Adding index on 'IdentifierTracker', fields ['hostname_modified']
#        db.create_index('bhp_identifier_identifiertracker', ['hostname_modified'])


    def backwards(self, orm):
        
        # Removing index on 'IdentifierTracker', fields ['hostname_modified']
        db.delete_index('bhp_identifier_identifiertracker', ['hostname_modified'])

        # Removing index on 'IdentifierTracker', fields ['hostname_created']
        db.delete_index('bhp_identifier_identifiertracker', ['hostname_created'])

        # Deleting model 'SubjectIdentifier'
        db.delete_table('bhp_identifier_subjectidentifier')


    models = {
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
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_identifier.subjectidentifier': {
            'Meta': {'object_name': 'SubjectIdentifier'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'default': '1000', 'unique': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_identifier']

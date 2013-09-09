# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IdentifierTracker'
         pass
#        db.create_table('bhp_identifier_identifiertracker', (
#            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
 #           ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
  #          ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
   #         ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
#            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
 #           ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
  #          ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
  #          ('identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
 #           ('identifier_string', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
 #           ('root_number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
 #           ('counter', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
 #           ('identifier_type', self.gf('django.db.models.fields.CharField')(max_length=35)),
 #       ))
 #       db.send_create_signal('bhp_identifier', ['IdentifierTracker'])
#
        # Adding unique constraint on 'IdentifierTracker', fields ['root_number', 'counter']
         db.create_unique('bhp_identifier_identifiertracker', ['root_number', 'counter'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'IdentifierTracker', fields ['root_number', 'counter']
        db.delete_unique('bhp_identifier_identifiertracker', ['root_number', 'counter'])

        # Deleting model 'IdentifierTracker'
        db.delete_table('bhp_identifier_identifiertracker')


    models = {
        'bhp_identifier.identifiertracker': {
            'Meta': {'ordering': "['root_number', 'counter']", 'unique_together': "(['root_number', 'counter'],)", 'object_name': 'IdentifierTracker'},
            'counter': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'identifier_string': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'identifier_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'root_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_identifier']

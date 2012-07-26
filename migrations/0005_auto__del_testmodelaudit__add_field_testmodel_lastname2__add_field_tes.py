# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestModelAudit'
        db.delete_table('bhp_crypto_testmodel_audit')

        # Adding field 'TestModel.lastname2'
        db.add_column('bhp_crypto_testmodel', 'lastname2',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=78L),
                      keep_default=False)

        # Adding field 'TestModel.char3'
        db.add_column('bhp_crypto_testmodel', 'char3',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=78L),
                      keep_default=False)

        # Adding field 'TestModel.firstname2'
        db.add_column('bhp_crypto_testmodel', 'firstname2',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=78L),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'TestModelAudit'
        db.create_table('bhp_crypto_testmodel_audit', (
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('text3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('char1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('bhp_crypto', ['TestModelAudit'])

        # Deleting field 'TestModel.lastname2'
        db.delete_column('bhp_crypto_testmodel', 'lastname2')

        # Deleting field 'TestModel.char3'
        db.delete_column('bhp_crypto_testmodel', 'char3')

        # Deleting field 'TestModel.firstname2'
        db.delete_column('bhp_crypto_testmodel', 'firstname2')


    models = {
        'bhp_crypto.crypt': {
            'Meta': {'object_name': 'Crypt'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'secret': ('django.db.models.fields.TextField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_crypto.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'char1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'firstname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'lastname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_crypto']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestModelAudit'
        db.delete_table('bhp_crypto_testmodel_audit')


    def backwards(self, orm):
        # Adding model 'TestModelAudit'
        db.create_table('bhp_crypto_testmodel_audit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('char1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('firstname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('lastname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_crypto', ['TestModelAudit'])


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
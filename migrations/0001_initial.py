# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AuditComment'
        db.create_table('audit_trail_auditcomment', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('audit_id', self.gf('django.db.models.fields.IntegerField')()),
            ('audit_comment', self.gf('django.db.models.fields.TextField')(max_length=250)),
        ))
        db.send_create_signal('audit_trail', ['AuditComment'])


    def backwards(self, orm):
        
        # Deleting model 'AuditComment'
        db.delete_table('audit_trail_auditcomment')


    models = {
        'audit_trail.auditcomment': {
            'Meta': {'object_name': 'AuditComment'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'audit_comment': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'audit_id': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['audit_trail']

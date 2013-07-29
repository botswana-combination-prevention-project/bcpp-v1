# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseReport'
        db.create_table('bhp_birt_reports_basereport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('report_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
        ))
        db.send_create_signal('bhp_birt_reports', ['BaseReport'])

        # Adding model 'ReportParameter'
        db.create_table('bhp_birt_reports_reportparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_birt_reports.BaseReport'])),
            ('parameter_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('parameter_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('is_selectfield', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('query_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_birt_reports', ['ReportParameter'])

        # Adding unique constraint on 'ReportParameter', fields ['report', 'parameter_name']
        db.create_unique('bhp_birt_reports_reportparameter', ['report_id', 'parameter_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'ReportParameter', fields ['report', 'parameter_name']
        db.delete_unique('bhp_birt_reports_reportparameter', ['report_id', 'parameter_name'])

        # Deleting model 'BaseReport'
        db.delete_table('bhp_birt_reports_basereport')

        # Deleting model 'ReportParameter'
        db.delete_table('bhp_birt_reports_reportparameter')


    models = {
        'bhp_birt_reports.basereport': {
            'Meta': {'object_name': 'BaseReport'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_birt_reports.reportparameter': {
            'Meta': {'unique_together': "(('report', 'parameter_name'),)", 'object_name': 'ReportParameter'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_selectfield': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parameter_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'parameter_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_birt_reports.BaseReport']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_birt_reports']
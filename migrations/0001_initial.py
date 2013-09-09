# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LabelPrinter'
        db.create_table('lab_barcode_labelprinter', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('cups_printer_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cups_server_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lab_barcode', ['LabelPrinter'])

        # Adding model 'Client'
        db.create_table('lab_barcode_client', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('label_printer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_barcode.LabelPrinter'])),
        ))
        db.send_create_signal('lab_barcode', ['Client'])

        # Adding model 'ZplTemplate'
        db.create_table('lab_barcode_zpltemplate', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lab_barcode', ['ZplTemplate'])


    def backwards(self, orm):
        
        # Deleting model 'LabelPrinter'
        db.delete_table('lab_barcode_labelprinter')

        # Deleting model 'Client'
        db.delete_table('lab_barcode_client')

        # Deleting model 'ZplTemplate'
        db.delete_table('lab_barcode_zpltemplate')


    models = {
        'lab_barcode.client': {
            'Meta': {'object_name': 'Client'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'label_printer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_barcode.LabelPrinter']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_barcode.labelprinter': {
            'Meta': {'object_name': 'LabelPrinter'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cups_printer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cups_server_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_barcode.zpltemplate': {
            'Meta': {'object_name': 'ZplTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_barcode']

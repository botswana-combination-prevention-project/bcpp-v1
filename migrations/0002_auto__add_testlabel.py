# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TestLabel'
        db.create_table('lab_barcode_testlabel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('lab_barcode', ['TestLabel'])

        # Adding index on 'LabelPrinter', fields ['hostname_created']
        db.create_index('lab_barcode_labelprinter', ['hostname_created'])

        # Adding index on 'LabelPrinter', fields ['hostname_modified']
        db.create_index('lab_barcode_labelprinter', ['hostname_modified'])

        # Adding index on 'ZplTemplate', fields ['hostname_created']
        db.create_index('lab_barcode_zpltemplate', ['hostname_created'])

        # Adding index on 'ZplTemplate', fields ['hostname_modified']
        db.create_index('lab_barcode_zpltemplate', ['hostname_modified'])

        # Adding index on 'Client', fields ['hostname_created']
        db.create_index('lab_barcode_client', ['hostname_created'])

        # Adding index on 'Client', fields ['hostname_modified']
        db.create_index('lab_barcode_client', ['hostname_modified'])


    def backwards(self, orm):
        
        # Removing index on 'Client', fields ['hostname_modified']
        db.delete_index('lab_barcode_client', ['hostname_modified'])

        # Removing index on 'Client', fields ['hostname_created']
        db.delete_index('lab_barcode_client', ['hostname_created'])

        # Removing index on 'ZplTemplate', fields ['hostname_modified']
        db.delete_index('lab_barcode_zpltemplate', ['hostname_modified'])

        # Removing index on 'ZplTemplate', fields ['hostname_created']
        db.delete_index('lab_barcode_zpltemplate', ['hostname_created'])

        # Removing index on 'LabelPrinter', fields ['hostname_modified']
        db.delete_index('lab_barcode_labelprinter', ['hostname_modified'])

        # Removing index on 'LabelPrinter', fields ['hostname_created']
        db.delete_index('lab_barcode_labelprinter', ['hostname_created'])

        # Deleting model 'TestLabel'
        db.delete_table('lab_barcode_testlabel')


    models = {
        'lab_barcode.client': {
            'Meta': {'ordering': "['ip', 'label_printer']", 'object_name': 'Client'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'label_printer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_barcode.LabelPrinter']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_barcode.labelprinter': {
            'Meta': {'ordering': "['cups_server_ip']", 'object_name': 'LabelPrinter'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cups_printer_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'cups_server_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_barcode.testlabel': {
            'Meta': {'ordering': "['identifier']", 'object_name': 'TestLabel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_barcode.zpltemplate': {
            'Meta': {'object_name': 'ZplTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'template': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_barcode']

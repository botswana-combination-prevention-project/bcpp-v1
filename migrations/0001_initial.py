# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TestCodeGroup'
        db.create_table('bhp_lab_test_code_testcodegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('lab_test_code', ['TestCodeGroup'])

        # Adding model 'TestCode'
        db.create_table('bhp_lab_test_code_testcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('test_code_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_test_code.TestCodeGroup'])),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('display_decimal_places', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reference_range_hi', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('reference_range_lo', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('lln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('uln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('is_absolute', self.gf('django.db.models.fields.CharField')(default='absolute', max_length='15')),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length='50', null=True, blank=True)),
        ))
        db.send_create_signal('lab_test_code', ['TestCode'])

        # Adding model 'TestCodeInterfaceMapping'
        db.create_table('bhp_lab_test_code_testcodeinterfacemapping', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('foreign_test_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('local_test_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_test_code.TestCode'])),
        ))
        db.send_create_signal('lab_test_code', ['TestCodeInterfaceMapping'])

        # Adding model 'TestCodeReferenceList'
        db.create_table('bhp_lab_test_code_testcodereferencelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('list_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('lab_test_code', ['TestCodeReferenceList'])

        # Adding model 'TestCodeReferenceListItem'
        db.create_table('bhp_lab_test_code_testcodereferencelistitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('test_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_test_code.TestCode'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('lln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=4, blank=True)),
            ('uln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=4, blank=True)),
            ('age_low', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_low_unit', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('age_low_quantifier', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('age_high', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_high_unit', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('age_high_quantifier', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('panic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=4, blank=True)),
            ('panic_value_quantifier', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('test_code_reference_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_test_code.TestCodeReferenceList'])),
        ))
        db.send_create_signal('lab_test_code', ['TestCodeReferenceListItem'])


    def backwards(self, orm):
        
        # Deleting model 'TestCodeGroup'
        db.delete_table('bhp_lab_test_code_testcodegroup')

        # Deleting model 'TestCode'
        db.delete_table('bhp_lab_test_code_testcode')

        # Deleting model 'TestCodeInterfaceMapping'
        db.delete_table('bhp_lab_test_code_testcodeinterfacemapping')

        # Deleting model 'TestCodeReferenceList'
        db.delete_table('bhp_lab_test_code_testcodereferencelist')

        # Deleting model 'TestCodeReferenceListItem'
        db.delete_table('bhp_lab_test_code_testcodereferencelistitem')


    models = {
        'lab_test_code.testcode': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_absolute': ('django.db.models.fields.CharField', [], {'default': "'absolute'", 'max_length': "'15'"}),
            'lln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference_range_hi': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'reference_range_lo': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'test_code_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCodeGroup']"}),
            'uln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcodegroup': {
            'Meta': {'object_name': 'TestCodeGroup'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcodeinterfacemapping': {
            'Meta': {'object_name': 'TestCodeInterfaceMapping'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'foreign_test_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCode']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcodereferencelist': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCodeReferenceList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcodereferencelistitem': {
            'Meta': {'ordering': "['test_code', 'age_low', 'age_low_unit']", 'object_name': 'TestCodeReferenceListItem'},
            'age_high': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_high_quantifier': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'age_high_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'age_low': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'age_low_quantifier': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'age_low_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_quantifier': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCode']"}),
            'test_code_reference_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCodeReferenceList']"}),
            'uln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_test_code']

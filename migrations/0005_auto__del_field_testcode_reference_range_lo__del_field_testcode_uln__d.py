# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TestCode.reference_range_lo'
        db.delete_column('bhp_lab_test_code_testcode', 'reference_range_lo')

        # Deleting field 'TestCode.uln'
        db.delete_column('bhp_lab_test_code_testcode', 'uln')

        # Deleting field 'TestCode.lln'
        db.delete_column('bhp_lab_test_code_testcode', 'lln')

        # Deleting field 'TestCode.reference_range_hi'
        db.delete_column('bhp_lab_test_code_testcode', 'reference_range_hi')


    def backwards(self, orm):
        
        # Adding field 'TestCode.reference_range_lo'
        db.add_column('bhp_lab_test_code_testcode', 'reference_range_lo', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=4), keep_default=False)

        # Adding field 'TestCode.uln'
        db.add_column('bhp_lab_test_code_testcode', 'uln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True), keep_default=False)

        # Adding field 'TestCode.lln'
        db.add_column('bhp_lab_test_code_testcode', 'lln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True), keep_default=False)

        # Adding field 'TestCode.reference_range_hi'
        db.add_column('bhp_lab_test_code_testcode', 'reference_range_hi', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=4), keep_default=False)


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
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'test_code_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCodeGroup']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCode']"}),
            'test_code_reference_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCodeReferenceList']"}),
            'uln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcodereferencelistitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestCodeReferenceListItemAudit', 'db_table': "'bhp_lab_test_code_testcodereferencelistitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'lln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testcodereferencelistitem'", 'to': "orm['lab_test_code.TestCode']"}),
            'test_code_reference_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testcodereferencelistitem'", 'to': "orm['lab_test_code.TestCodeReferenceList']"}),
            'uln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_test_code']

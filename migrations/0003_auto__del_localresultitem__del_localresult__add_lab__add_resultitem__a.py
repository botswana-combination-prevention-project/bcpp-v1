# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'LocalResultItem'
        db.delete_table('lab_clinic_api_localresultitem')

        # Deleting model 'LocalResult'
        db.delete_table('lab_clinic_api_localresult')

        # Adding model 'Lab'
        db.create_table('lab_clinic_api_lab', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('release_status', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('panel', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('aliquot_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('receive_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('release_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('lab_clinic_api', ['Lab'])

        # Adding model 'ResultItem'
        db.create_table('lab_clinic_api_resultitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('result_item_value', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('result_item_quantifier', self.gf('django.db.models.fields.CharField')(default='=', max_length=25)),
            ('result_item_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('result_item_operator', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, null=True, blank=True)),
            ('grade_range', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('grade_flag', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('reference_flag', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('reference_range', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('validation_status', self.gf('django.db.models.fields.CharField')(default='P', max_length=10, db_index=True)),
            ('validation_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('validation_username', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, null=True, blank=True)),
            ('validation_reference', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('error_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('test_code', self.gf('django.db.models.fields.related.ForeignKey')(related_name='test_code_clinic', to=orm['lab_test_code.TestCode'])),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_clinic_api.Result'])),
        ))
        db.send_create_signal('lab_clinic_api', ['ResultItem'])

        # Adding model 'Result'
        db.create_table('lab_clinic_api_result', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('result_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('result_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('release_status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=25, db_index=True)),
            ('release_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('release_username', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('dmis_result_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_clinic_api.Lab'])),
        ))
        db.send_create_signal('lab_clinic_api', ['Result'])

        # Deleting field 'Review.local_result'
        db.delete_column('lab_clinic_api_review', 'local_result_id')

        # Adding field 'Review.lab'
        db.add_column('lab_clinic_api_review', 'lab', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['lab_clinic_api.Lab']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'LocalResultItem'
        db.create_table('lab_clinic_api_localresultitem', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('test_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_test_code.TestCode'])),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('validation_status', self.gf('django.db.models.fields.CharField')(default='P', max_length=10, db_index=True)),
            ('validation_datetime', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('result_item_value', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('validation_username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, null=True, db_index=True)),
            ('result_item_quantifier', self.gf('django.db.models.fields.CharField')(default='=', max_length=25)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('result_item_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('result_item_operator', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, null=True, db_index=True)),
            ('validation_reference', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('local_result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_clinic_api.LocalResult'])),
            ('error_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('lab_clinic_api', ['LocalResultItem'])

        # Adding model 'LocalResult'
        db.create_table('lab_clinic_api_localresult', (
            ('release_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('aliquot_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('receive_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('release_status', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('panel', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('lab_clinic_api', ['LocalResult'])

        # Deleting model 'Lab'
        db.delete_table('lab_clinic_api_lab')

        # Deleting model 'ResultItem'
        db.delete_table('lab_clinic_api_resultitem')

        # Deleting model 'Result'
        db.delete_table('lab_clinic_api_result')

        # User chose to not deal with backwards NULL issues for 'Review.local_result'
        raise RuntimeError("Cannot reverse this migration. 'Review.local_result' and its values cannot be restored.")

        # Deleting field 'Review.lab'
        db.delete_column('lab_clinic_api_review', 'lab_id')


    models = {
        'lab_clinic_api.lab': {
            'Meta': {'object_name': 'Lab'},
            'aliquot_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'panel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'receive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'release_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'release_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_clinic_api.result': {
            'Meta': {'object_name': 'Result'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dmis_result_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Lab']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'release_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'release_status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '25', 'db_index': 'True'}),
            'release_username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'result_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'result_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_clinic_api.resultitem': {
            'Meta': {'object_name': 'ResultItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'grade_flag': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'grade_range': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reference_flag': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'reference_range': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Result']"}),
            'result_item_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'result_item_operator': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'result_item_quantifier': ('django.db.models.fields.CharField', [], {'default': "'='", 'max_length': '25'}),
            'result_item_value': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_code_clinic'", 'to': "orm['lab_test_code.TestCode']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'validation_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'validation_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '10', 'db_index': 'True'}),
            'validation_username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'lab_clinic_api.review': {
            'Meta': {'object_name': 'Review'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Lab']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'review_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'review_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REVIEWED'", 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_test_code.testcode': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCode', 'db_table': "'bhp_lab_test_code_testcode'"},
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
            'Meta': {'ordering': "['code']", 'object_name': 'TestCodeGroup', 'db_table': "'bhp_lab_test_code_testcodegroup'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_clinic_api']

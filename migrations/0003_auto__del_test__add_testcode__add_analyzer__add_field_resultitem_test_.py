# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Test'
        db.delete_table('bhp_lab_test')

        # Adding model 'TestCode'
        db.create_table('bhp_lab_testcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab.TestGroup'])),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reference_range_hi', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('reference_range_lo', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('display_decimal_places', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('uln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('is_absolute', self.gf('django.db.models.fields.CharField')(default='ABS', max_length='5')),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length='50', null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bhp_lab', ['TestCode'])

        # Adding model 'Analyzer'
        db.create_table('bhp_lab_analyzer', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bhp_lab', ['Analyzer'])

        # Adding M2M table for field panel on 'Analyzer'
        db.create_table('bhp_lab_analyzer_panel', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analyzer', models.ForeignKey(orm['bhp_lab.analyzer'], null=False)),
            ('panel', models.ForeignKey(orm['bhp_lab.panel'], null=False))
        ))
        db.create_unique('bhp_lab_analyzer_panel', ['analyzer_id', 'panel_id'])

        # Adding field 'ResultItem.test_code'
        db.add_column('bhp_lab_resultitem', 'test_code', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bhp_lab.TestCode']), keep_default=False)

        # Adding field 'ResultItem.result_value'
        db.add_column('bhp_lab_resultitem', 'result_value', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'ResultItem.result_quantifier'
        db.add_column('bhp_lab_resultitem', 'result_quantifier', self.gf('django.db.models.fields.CharField')(default='=', max_length=25), keep_default=False)

        # Adding field 'ResultItem.status'
        db.add_column('bhp_lab_resultitem', 'status', self.gf('django.db.models.fields.CharField')(default='P', max_length=10), keep_default=False)

        # Adding field 'ResultItem.error_code'
        db.add_column('bhp_lab_resultitem', 'error_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'ResultItem.comment'
        db.add_column('bhp_lab_resultitem', 'comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Result.assay_date'
        db.add_column('bhp_lab_result', 'assay_date', self.gf('django.db.models.fields.DateTimeField')(default=0), keep_default=False)

        # Adding field 'Result.analyzer'
        db.add_column('bhp_lab_result', 'analyzer', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bhp_lab.Analyzer']), keep_default=False)

        # Adding field 'Result.source'
        db.add_column('bhp_lab_result', 'source', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Result.archive'
        db.add_column('bhp_lab_result', 'archive', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Result.comment'
        db.add_column('bhp_lab_result', 'comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Changing field 'TestMap.local_test_code'
        db.alter_column('bhp_lab_testmap', 'local_test_code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab.TestCode']))


    def backwards(self, orm):
        
        # Adding model 'Test'
        db.create_table('bhp_lab_test', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('reference_range_lo', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('display_decimal_places', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_code', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True)),
            ('test_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab.TestGroup'])),
            ('uln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('lln', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('test_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length='50', null=True, blank=True)),
            ('reference_range_hi', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=4)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('is_absolute', self.gf('django.db.models.fields.CharField')(default='ABS', max_length='5')),
        ))
        db.send_create_signal('bhp_lab', ['Test'])

        # Deleting model 'TestCode'
        db.delete_table('bhp_lab_testcode')

        # Deleting model 'Analyzer'
        db.delete_table('bhp_lab_analyzer')

        # Removing M2M table for field panel on 'Analyzer'
        db.delete_table('bhp_lab_analyzer_panel')

        # Deleting field 'ResultItem.test_code'
        db.delete_column('bhp_lab_resultitem', 'test_code_id')

        # Deleting field 'ResultItem.result_value'
        db.delete_column('bhp_lab_resultitem', 'result_value')

        # Deleting field 'ResultItem.result_quantifier'
        db.delete_column('bhp_lab_resultitem', 'result_quantifier')

        # Deleting field 'ResultItem.status'
        db.delete_column('bhp_lab_resultitem', 'status')

        # Deleting field 'ResultItem.error_code'
        db.delete_column('bhp_lab_resultitem', 'error_code')

        # Deleting field 'ResultItem.comment'
        db.delete_column('bhp_lab_resultitem', 'comment')

        # Deleting field 'Result.assay_date'
        db.delete_column('bhp_lab_result', 'assay_date')

        # Deleting field 'Result.analyzer'
        db.delete_column('bhp_lab_result', 'analyzer_id')

        # Deleting field 'Result.source'
        db.delete_column('bhp_lab_result', 'source')

        # Deleting field 'Result.archive'
        db.delete_column('bhp_lab_result', 'archive')

        # Deleting field 'Result.comment'
        db.delete_column('bhp_lab_result', 'comment')

        # Changing field 'TestMap.local_test_code'
        db.alter_column('bhp_lab_testmap', 'local_test_code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab.Test']))


    models = {
        'bhp_lab.aliquot': {
            'Meta': {'object_name': 'Aliquot'},
            'aliquot_condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.AliquotCondition']"}),
            'aliquot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.AliquotType']"}),
            'aliquot_volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'id_int': ('django.db.models.fields.IntegerField', [], {}),
            'id_seed': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.aliquotcondition': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'AliquotCondition'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab.aliquottype': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'AliquotType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab.analyzer': {
            'Meta': {'object_name': 'Analyzer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'panel': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab.Panel']", 'symmetrical': 'False'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.order': {
            'Meta': {'object_name': 'Order'},
            'aliquot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.Aliquot']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.Panel']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.panel': {
            'Meta': {'object_name': 'Panel'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'test': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab.TestCode']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.receive': {
            'Meta': {'object_name': 'Receive'},
            'aliquot': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_lab.Aliquot']", 'unique': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_drawn': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_received': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.result': {
            'Meta': {'object_name': 'Result'},
            'analyzer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.Analyzer']"}),
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'assay_date': ('django.db.models.fields.DateTimeField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.Order']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.resultitem': {
            'Meta': {'object_name': 'ResultItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.Result']"}),
            'result_quantifier': ('django.db.models.fields.CharField', [], {'default': "'='", 'max_length': '25'}),
            'result_value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '10'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.TestCode']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.testcode': {
            'Meta': {'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.TestGroup']"}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_absolute': ('django.db.models.fields.CharField', [], {'default': "'ABS'", 'max_length': "'5'"}),
            'lln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reference_range_hi': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'reference_range_lo': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'uln': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab.testgroup': {
            'Meta': {'object_name': 'TestGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab.testmap': {
            'Meta': {'object_name': 'TestMap'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'foreign_test_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab.TestCode']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_registration.registeredsubject': {
            'Meta': {'object_name': 'RegisteredSubject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_lab']

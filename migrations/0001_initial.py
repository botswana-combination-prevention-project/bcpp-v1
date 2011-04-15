# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SpecimenType'
        db.create_table('bhp_lab_core_specimentype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_lab_core', ['SpecimenType'])

        # Adding model 'AliquotType'
        db.create_table('bhp_lab_core_aliquottype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_lab_core', ['AliquotType'])

        # Adding model 'AliquotCondition'
        db.create_table('bhp_lab_core_aliquotcondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_lab_core', ['AliquotCondition'])

        # Adding model 'Aliquot'
        db.create_table('bhp_lab_core_aliquot', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('aliquot_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('aliquot_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.AliquotType'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.AliquotCondition'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bhp_lab_core', ['Aliquot'])

        # Adding model 'TestGroup'
        db.create_table('bhp_lab_core_testgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_lab_core', ['TestGroup'])

        # Adding model 'TestCode'
        db.create_table('bhp_lab_core_testcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.TestGroup'])),
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
        db.send_create_signal('bhp_lab_core', ['TestCode'])

        # Adding model 'TestMap'
        db.create_table('bhp_lab_core_testmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('foreign_test_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('local_test_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.TestCode'])),
        ))
        db.send_create_signal('bhp_lab_core', ['TestMap'])

        # Adding model 'Panel'
        db.create_table('bhp_lab_core_panel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bhp_lab_core', ['Panel'])

        # Adding M2M table for field test_code on 'Panel'
        db.create_table('bhp_lab_core_panel_test_code', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panel', models.ForeignKey(orm['bhp_lab_core.panel'], null=False)),
            ('testcode', models.ForeignKey(orm['bhp_lab_core.testcode'], null=False))
        ))
        db.create_unique('bhp_lab_core_panel_test_code', ['panel_id', 'testcode_id'])

        # Adding model 'Analyzer'
        db.create_table('bhp_lab_core_analyzer', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bhp_lab_core', ['Analyzer'])

        # Adding M2M table for field panel on 'Analyzer'
        db.create_table('bhp_lab_core_analyzer_panel', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analyzer', models.ForeignKey(orm['bhp_lab_core.analyzer'], null=False)),
            ('panel', models.ForeignKey(orm['bhp_lab_core.panel'], null=False))
        ))
        db.create_unique('bhp_lab_core_analyzer_panel', ['analyzer_id', 'panel_id'])

        # Adding model 'Order'
        db.create_table('bhp_lab_core_order', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('order_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('order_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('aliquot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.Aliquot'])),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.Panel'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_lab_core', ['Order'])

        # Adding model 'Receive'
        db.create_table('bhp_lab_core_receive', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('receive_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_registration.Patient'])),
            ('datetime_drawn', self.gf('django.db.models.fields.DateTimeField')()),
            ('specimen_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.SpecimenType'])),
            ('specimen_medium', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('specimen_measure', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('specimen_measure_units', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('datetime_received', self.gf('django.db.models.fields.DateTimeField')()),
            ('aliquot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.Aliquot'])),
        ))
        db.send_create_signal('bhp_lab_core', ['Receive'])

        # Adding model 'Result'
        db.create_table('bhp_lab_core_result', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('result_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('assay_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('analyzer', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_lab_core', ['Result'])

        # Adding model 'ResultItem'
        db.create_table('bhp_lab_core_resultitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_lab_core.Result'])),
            ('test_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('result_value', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('result_quantifier', self.gf('django.db.models.fields.CharField')(default='=', max_length=25)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=10)),
            ('error_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_lab_core', ['ResultItem'])


    def backwards(self, orm):
        # Deleting model 'SpecimenType'
        db.delete_table('bhp_lab_core_specimentype')

        # Deleting model 'AliquotType'
        db.delete_table('bhp_lab_core_aliquottype')

        # Deleting model 'AliquotCondition'
        db.delete_table('bhp_lab_core_aliquotcondition')

        # Deleting model 'Aliquot'
        db.delete_table('bhp_lab_core_aliquot')

        # Deleting model 'TestGroup'
        db.delete_table('bhp_lab_core_testgroup')

        # Deleting model 'TestCode'
        db.delete_table('bhp_lab_core_testcode')

        # Deleting model 'TestMap'
        db.delete_table('bhp_lab_core_testmap')

        # Deleting model 'Panel'
        db.delete_table('bhp_lab_core_panel')

        # Removing M2M table for field test_code on 'Panel'
        db.delete_table('bhp_lab_core_panel_test_code')

        # Deleting model 'Analyzer'
        db.delete_table('bhp_lab_core_analyzer')

        # Removing M2M table for field panel on 'Analyzer'
        db.delete_table('bhp_lab_core_analyzer_panel')

        # Deleting model 'Order'
        db.delete_table('bhp_lab_core_order')

        # Deleting model 'Receive'
        db.delete_table('bhp_lab_core_receive')

        # Deleting model 'Result'
        db.delete_table('bhp_lab_core_result')

        # Deleting model 'ResultItem'
        db.delete_table('bhp_lab_core_resultitem')


    models = {
        'bhp_lab_core.aliquot': {
            'Meta': {'object_name': 'Aliquot'},
            'aliquot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.AliquotType']"}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.AliquotCondition']"}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'bhp_lab_core.aliquotcondition': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'AliquotCondition'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab_core.aliquottype': {
            'Meta': {'ordering': "['short_name']", 'object_name': 'AliquotType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab_core.analyzer': {
            'Meta': {'object_name': 'Analyzer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'panel': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab_core.Panel']", 'symmetrical': 'False'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.order': {
            'Meta': {'object_name': 'Order'},
            'aliquot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.Aliquot']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.Panel']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.panel': {
            'Meta': {'object_name': 'Panel'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab_core.TestCode']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.receive': {
            'Meta': {'object_name': 'Receive'},
            'aliquot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.Aliquot']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_drawn': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_received': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_registration.Patient']"}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'specimen_measure': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'specimen_measure_units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'specimen_medium': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'specimen_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.SpecimenType']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.result': {
            'Meta': {'object_name': 'Result'},
            'analyzer': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'assay_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'result_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.resultitem': {
            'Meta': {'object_name': 'ResultItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.Result']"}),
            'result_quantifier': ('django.db.models.fields.CharField', [], {'default': "'='", 'max_length': '25'}),
            'result_value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '10'}),
            'test_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_core.specimentype': {
            'Meta': {'object_name': 'SpecimenType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab_core.testcode': {
            'Meta': {'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.TestGroup']"}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
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
        'bhp_lab_core.testgroup': {
            'Meta': {'object_name': 'TestGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_lab_core.testmap': {
            'Meta': {'object_name': 'TestMap'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'foreign_test_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_lab_core.TestCode']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_registration.account': {
            'Meta': {'ordering': "['account_name']", 'object_name': 'Account'},
            'account_closedate': ('django.db.models.fields.DateField', [], {}),
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'account_opendate': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'principal_investigator': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.PrincipalInvestigator']", 'symmetrical': 'False'}),
            'site_leader': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.SiteLeader']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_registration.patient': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(['subject_identifier'],)", 'object_name': 'Patient'},
            'account': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab_registration.Account']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'simple_consent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_lab_registration.SimpleConsent']", 'symmetrical': 'False'}),
            'study_site': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_variables.StudySite']", 'symmetrical': 'False'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_lab_registration.simpleconsent': {
            'Meta': {'ordering': "['consent_startdate']", 'object_name': 'SimpleConsent'},
            'consent_enddate': ('django.db.models.fields.DateField', [], {}),
            'consent_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'consent_startdate': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_research_protocol.Protocol']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_research_protocol.fundingsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'FundingSource'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'bhp_research_protocol.principalinvestigator': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'PrincipalInvestigator'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_research_protocol.protocol': {
            'Meta': {'ordering': "['protocol_identifier']", 'object_name': 'Protocol'},
            'date_opened': ('django.db.models.fields.DateField', [], {}),
            'date_registered': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'funding_source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.FundingSource']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_title': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'prinicipal_investigator': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.PrincipalInvestigator']", 'symmetrical': 'False'}),
            'protocol_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'research_title': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site_leader': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.SiteLeader']", 'symmetrical': 'False'})
        },
        'bhp_research_protocol.siteleader': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'SiteLeader'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_variables.studysite': {
            'Meta': {'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_lab_core']

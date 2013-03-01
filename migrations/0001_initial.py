# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestRequisitionAudit'
        db.create_table('lab_requisition_testrequisition_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('requisition_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('requisition_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('specimen_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['bhp_variables.StudySite'])),
            ('clinician_initials', self.gf('django.db.models.fields.CharField')(default='--', max_length=3, null=True, blank=True)),
            ('aliquot_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['lab_aliquot_list.AliquotType'])),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['lab_panel.Panel'])),
            ('priority', self.gf('django.db.models.fields.CharField')(default='normal', max_length=25)),
            ('is_drawn', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('reason_not_drawn', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='tube', max_length=25)),
            ('item_count_total', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('estimated_volume', self.gf('django.db.models.fields.DecimalField')(default=5.0, max_digits=7, decimal_places=1)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=25, null=True, blank=True)),
            ('is_receive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_packed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_lis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('lab_requisition', ['TestRequisitionAudit'])

        # Adding model 'TestRequisition'
        db.create_table('lab_requisition_testrequisition', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('requisition_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('requisition_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('specimen_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True, null=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('clinician_initials', self.gf('django.db.models.fields.CharField')(default='--', max_length=3, null=True, blank=True)),
            ('aliquot_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_aliquot_list.AliquotType'])),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_panel.Panel'])),
            ('priority', self.gf('django.db.models.fields.CharField')(default='normal', max_length=25)),
            ('is_drawn', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('reason_not_drawn', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='tube', max_length=25)),
            ('item_count_total', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('estimated_volume', self.gf('django.db.models.fields.DecimalField')(default=5.0, max_digits=7, decimal_places=1)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=25, null=True, blank=True)),
            ('is_receive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_packed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_lis', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lab_requisition', ['TestRequisition'])

        # Adding M2M table for field test_code on 'TestRequisition'
        db.create_table('lab_requisition_testrequisition_test_code', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testrequisition', models.ForeignKey(orm['lab_requisition.testrequisition'], null=False)),
            ('testcode', models.ForeignKey(orm['lab_test_code.testcode'], null=False))
        ))
        db.create_unique('lab_requisition_testrequisition_test_code', ['testrequisition_id', 'testcode_id'])


    def backwards(self, orm):
        # Deleting model 'TestRequisitionAudit'
        db.delete_table('lab_requisition_testrequisition_audit')

        # Deleting model 'TestRequisition'
        db.delete_table('lab_requisition_testrequisition')

        # Removing M2M table for field test_code on 'TestRequisition'
        db.delete_table('lab_requisition_testrequisition_test_code')


    models = {
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_account.account': {
            'Meta': {'ordering': "['account_name']", 'object_name': 'Account', 'db_table': "'bhp_lab_registration_account'"},
            'account_closedate': ('django.db.models.fields.DateField', [], {}),
            'account_holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_account.AccountHolder']", 'null': 'True', 'blank': 'True'}),
            'account_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'account_opendate': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_account.accountholder': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'AccountHolder', 'db_table': "'bhp_lab_registration_accountholder'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_aliquot_list.aliquottype': {
            'Meta': {'ordering': "['name']", 'object_name': 'AliquotType', 'db_table': "'bhp_lab_core_aliquottype'"},
            'alpha_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dmis_reference': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_panel.panel': {
            'Meta': {'ordering': "['name']", 'object_name': 'Panel', 'db_table': "'bhp_lab_core_panel'"},
            'account': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab_account.Account']", 'null': 'True', 'blank': 'True'}),
            'aliquot_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lab_aliquot_list.AliquotType']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dmis_panel_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'panel_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_panel.PanelGroup']"}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lab_test_code.TestCode']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_panel.panelgroup': {
            'Meta': {'object_name': 'PanelGroup', 'db_table': "'bhp_lab_core_panelgroup'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_requisition.testrequisition': {
            'Meta': {'object_name': 'TestRequisition'},
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_aliquot_list.AliquotType']"}),
            'clinician_initials': ('django.db.models.fields.CharField', [], {'default': "'--'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_volume': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '7', 'decimal_places': '1'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_drawn': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_labelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_labelled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_lis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_packed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'item_count_total': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'tube'", 'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_panel.Panel']"}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '25'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reason_not_drawn': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'requisition_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'requisition_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'specimen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab_test_code.TestCode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_requisition.testrequisitionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestRequisitionAudit', 'db_table': "'lab_requisition_testrequisition_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['lab_aliquot_list.AliquotType']"}),
            'clinician_initials': ('django.db.models.fields.CharField', [], {'default': "'--'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_volume': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '7', 'decimal_places': '1'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_drawn': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_labelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_labelled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_lis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_packed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'item_count_total': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'tube'", 'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['lab_panel.Panel']"}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '25'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reason_not_drawn': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'requisition_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'requisition_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['bhp_variables.StudySite']"}),
            'specimen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_test_code.testcode': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCode', 'db_table': "'bhp_lab_test_code_testcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_absolute': ('django.db.models.fields.CharField', [], {'default': "'absolute'", 'max_length': "'15'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'test_code_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_test_code.TestCodeGroup']"}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_test_code.testcodegroup': {
            'Meta': {'ordering': "['code']", 'object_name': 'TestCodeGroup', 'db_table': "'bhp_lab_test_code_testcodegroup'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['lab_requisition']
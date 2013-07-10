# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Household', fields ['ward']
        db.delete_unique('bcpp_household_household', ['ward_id'])
 
        # Removing unique constraint on 'HouseholdStructureMember', fields ['registered_subject', 'household_structure']
        db.delete_unique('bcpp_household_householdstructuremember', ['registered_subject_id', 'household_structure_id'])
 
        # Removing unique constraint on 'HouseholdStructureMember', fields ['household_structure', 'first_name', 'initials']
        db.delete_unique('bcpp_household_householdstructuremember', ['household_structure_id', 'first_name', 'initials'])
 
        # Removing unique constraint on 'HouseholdSurveyReport', fields ['household_survey', 'survey_date', 'survey_start_time']
        db.delete_unique('bcpp_household_householdsurveyreport', ['household_survey_id', 'survey_date', 'survey_start_time'])
 
        # Removing unique constraint on 'HouseholdSurvey', fields ['household', 'survey_code']
        db.delete_unique('bcpp_householdsurvey', ['household_id', 'survey_code_id'])
 
        # Deleting model 'HouseholdSurvey'
        db.delete_table('bcpp_householdsurvey')
 
        # Deleting model 'HouseholdSurveyReport'
        db.delete_table('bcpp_household_householdsurveyreport')
 
        # Deleting model 'HouseholdStructureMemberAudit'
        db.delete_table('bcpp_household_householdstructuremember_audit')
 
        # Deleting model 'HouseholdStructureMember'
        db.delete_table('bcpp_household_householdstructuremember')

        # Deleting model 'Ward'
        db.delete_table('bcpp_household_ward')
        # Renaming column for 'HouseholdAudit.ward' to match new field type.
        db.rename_column('bcpp_household_household_audit', 'ward_id', 'ward')
        # Changing field 'HouseholdAudit.ward'
        db.alter_column('bcpp_household_household_audit', 'ward', self.gf('django.db.models.fields.CharField')(max_length=25))
 
        # Changing field 'Household.gps_device'
        db.alter_column('bcpp_household_household', 'gps_device_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.GpsDevice'], unique=True))
        # Adding unique constraint on 'Household', fields ['gps_device']
        db.create_unique('bcpp_household_household', ['gps_device_id'])
 

        # Renaming column for 'Household.ward' to match new field type.
        db.rename_column('bcpp_household_household', 'ward_id', 'ward')
        # Changing field 'Household.ward'
        db.alter_column('bcpp_household_household', 'ward', self.gf('django.db.models.fields.CharField')(max_length=25))

    def backwards(self, orm):
        # Removing unique constraint on 'Household', fields ['gps_device']
        db.delete_unique('bcpp_household_household', ['gps_device_id'])

        # Adding model 'HouseholdSurvey'
        db.create_table('bcpp_householdsurvey', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Household'])),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('survey_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.HouseholdSurveyCode'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdSurvey'])

        # Adding unique constraint on 'HouseholdSurvey', fields ['household', 'survey_code']
        db.create_unique('bcpp_householdsurvey', ['household_id', 'survey_code_id'])

        # Adding model 'HouseholdSurveyReport'
        db.create_table('bcpp_household_householdsurveyreport', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('survey_date', self.gf('django.db.models.fields.DateField')()),
            ('survey_start_time', self.gf('django.db.models.fields.TimeField')()),
            ('household_survey_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.HouseholdSurveyStatus'])),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('survey_end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('household_survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdSurvey'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdSurveyReport'])

        # Adding unique constraint on 'HouseholdSurveyReport', fields ['household_survey', 'survey_date', 'survey_start_time']
        db.create_unique('bcpp_household_householdsurveyreport', ['household_survey_id', 'survey_date', 'survey_start_time'])

        # Adding model 'HouseholdStructureMemberAudit'
        db.create_table('bcpp_household_householdstructuremember_audit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('is_eligible_member', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('member_status', self.gf('django.db.models.fields.CharField')(default='NOT_REPORTED', max_length=25, null=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('age_in_years', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('contact_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', null=True, to=orm['bcpp_household.ContactLog'])),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', null=True, to=orm['bhp_registration.RegisteredSubject'])),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('hiv_history', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', null=True, to=orm['bcpp_household.HouseholdStructure'], blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('internal_identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=36, null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', to=orm['bcpp_survey.Survey'])),
            ('lives_in_household', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureMemberAudit'])

        # Adding model 'HouseholdStructureMember'
        db.create_table('bcpp_household_householdstructuremember', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('is_eligible_member', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('member_status', self.gf('django.db.models.fields.CharField')(default='NOT_REPORTED', max_length=25, null=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('age_in_years', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('contact_log', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.ContactLog'], unique=True, null=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('hiv_history', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdStructure'], null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('internal_identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=36, null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('lives_in_household', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureMember'])

        # Adding unique constraint on 'HouseholdStructureMember', fields ['household_structure', 'first_name', 'initials']
        db.create_unique('bcpp_household_householdstructuremember', ['household_structure_id', 'first_name', 'initials'])

        # Adding unique constraint on 'HouseholdStructureMember', fields ['registered_subject', 'household_structure']
        db.create_unique('bcpp_household_householdstructuremember', ['registered_subject_id', 'household_structure_id'])

        # Adding model 'Ward'
        db.create_table('bcpp_household_ward', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('ward_name', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['Ward'])


        # Renaming column for 'HouseholdAudit.ward' to match new field type.
        db.rename_column('bcpp_household_household_audit', 'ward', 'ward_id')
        # Changing field 'HouseholdAudit.ward'
        db.alter_column('bcpp_household_household_audit', 'ward_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Ward']))

        # Changing field 'Household.gps_device'
        db.alter_column('bcpp_household_household', 'gps_device_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.GpsDevice']))

        # Renaming column for 'Household.ward' to match new field type.
        db.rename_column('bcpp_household_household', 'ward', 'ward_id')
        # Changing field 'Household.ward'
        db.alter_column('bcpp_household_household', 'ward_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.Ward'], unique=True))
        # Adding unique constraint on 'Household', fields ['ward']
        db.create_unique('bcpp_household_household', ['ward_id'])


    models = {
        'bcpp_household.contactlog': {
            'Meta': {'object_name': 'ContactLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.contactlogitem': {
            'Meta': {'object_name': 'ContactLogItem'},
            'appointment_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contact_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'contact_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.ContactLog']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'information_provider': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'is_contacted': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'subject_status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'try_again': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.gpsdevice': {
            'Meta': {'object_name': 'GpsDevice'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gps_make': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gps_model': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gps_purchase_date': ('django.db.models.fields.DateField', [], {}),
            'gps_purchase_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'gps_serial_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'gps_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'gps_device': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.GpsDevice']", 'unique': 'True'}),
            'gps_point_1': ('django.db.models.fields.CharField', [], {'default': '24', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_11': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_point_2': ('django.db.models.fields.CharField', [], {'default': '26', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_21': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_waypoint': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'ward_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'was_surveyed_previously': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '10'})
        },
        'bcpp_household.householdaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdAudit', 'db_table': "'bcpp_household_household_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'gps_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'gps_device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_household'", 'to': "orm['bcpp_household.GpsDevice']"}),
            'gps_point_1': ('django.db.models.fields.CharField', [], {'default': '24', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_11': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_point_2': ('django.db.models.fields.CharField', [], {'default': '26', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_21': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_waypoint': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'ward_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'was_surveyed_previously': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '10'})
        },
        'bcpp_household.householdidentifier': {
            'Meta': {'object_name': 'HouseholdIdentifier'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'is_derived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'sequence_app_label': ('django.db.models.fields.CharField', [], {'default': "'bhp_identifier'", 'max_length': '50'}),
            'sequence_model_name': ('django.db.models.fields.CharField', [], {'default': "'sequence'", 'max_length': '50'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlog': {
            'Meta': {'unique_together': "(('household', 'survey'),)", 'object_name': 'HouseholdLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdLogAudit', 'db_table': "'bcpp_household_householdlog_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdlog'", 'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdlog'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogentry': {
            'Meta': {'unique_together': "(('household_log', 'report_datetime'),)", 'object_name': 'HouseholdLogEntry'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hbc': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdLog']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogentryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdLogEntryAudit', 'db_table': "'bcpp_household_householdlogentry_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hbc': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdlogentry'", 'to': "orm['bcpp_household.HouseholdLog']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructure': {
            'Meta': {'unique_together': "(('household', 'survey'),)", 'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructureaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdStructureAudit', 'db_table': "'bcpp_household_householdstructure_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_list.surveygroup': {
            'Meta': {'object_name': 'SurveyGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_survey.survey': {
            'Meta': {'ordering': "['survey_name']", 'unique_together': "(('survey_name', 'survey_group'), ('survey_group', 'chronological_order'))", 'object_name': 'Survey'},
            'chronological_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SurveyGroup']"}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bcpp_household']
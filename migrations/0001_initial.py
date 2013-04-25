# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GpsDevice'
        db.create_table('bcpp_household_gpsdevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
            ('gps_make', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gps_model', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gps_serial_number', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gps_purchase_date', self.gf('django.db.models.fields.DateField')()),
            ('gps_purchase_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('bcpp_household', ['GpsDevice'])

        # Adding model 'HouseholdAudit'
        db.create_table('bcpp_household_household_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('household_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('hh_int', self.gf('django.db.models.fields.IntegerField')()),
            ('hh_seed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gps_device', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_household', to=orm['bcpp_household.GpsDevice'])),
            ('gps_waypoint', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gps_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('gps_point_1', self.gf('django.db.models.fields.CharField')(default=24, max_length=78L, db_index=True)),
            ('gps_point_11', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('gps_point_2', self.gf('django.db.models.fields.CharField')(default=26, max_length=78L, db_index=True)),
            ('gps_point_21', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('cso_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=78L, null=True, blank=True)),
            ('village', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('ward_section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('was_surveyed_previously', self.gf('django.db.models.fields.CharField')(default='No', max_length=10)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uploaded_map', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdAudit'])

        # Adding model 'Household'
        db.create_table('bcpp_household_household', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, db_index=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('hh_int', self.gf('django.db.models.fields.IntegerField')()),
            ('hh_seed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gps_device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.GpsDevice'])),
            ('gps_waypoint', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gps_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('gps_point_1', self.gf('django.db.models.fields.CharField')(default=24, max_length=78L, db_index=True)),
            ('gps_point_11', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('gps_point_2', self.gf('django.db.models.fields.CharField')(default=26, max_length=78L, db_index=True)),
            ('gps_point_21', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('cso_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=78L, null=True, blank=True)),
            ('village', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('ward_section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('was_surveyed_previously', self.gf('django.db.models.fields.CharField')(default='No', max_length=10)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uploaded_map', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bcpp_household', ['Household'])

        # Adding M2M table for field ward on 'Household'
        db.create_table('bcpp_household_household_ward', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('household', models.ForeignKey(orm['bcpp_household.household'], null=False)),
            ('bcppwards', models.ForeignKey(orm['bcpp_list.bcppwards'], null=False))
        ))
        db.create_unique('bcpp_household_household_ward', ['household_id', 'bcppwards_id'])

        # Adding model 'ContactLog'
        db.create_table('bcpp_household_contactlog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['ContactLog'])

        # Adding model 'ContactLogItem'
        db.create_table('bcpp_household_contactlogitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('contact_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.ContactLog'])),
            ('contact_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('subject_status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_contacted', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('information_provider', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('appointment_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('try_again', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['ContactLogItem'])

        # Adding model 'HouseholdStructureAudit'
        db.create_table('bcpp_household_householdstructure_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructure', to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructure', to=orm['bcpp_survey.Survey'])),
            ('member_count', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureAudit'])

        # Adding model 'HouseholdStructure'
        db.create_table('bcpp_household_householdstructure', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('member_count', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructure'])

        # Adding unique constraint on 'HouseholdStructure', fields ['household', 'survey']
        db.create_unique('bcpp_household_householdstructure', ['household_id', 'survey_id'])

        # Adding model 'HouseholdStructureMemberAudit'
        db.create_table('bcpp_household_householdstructuremember_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', null=True, to=orm['bhp_registration.RegisteredSubject'])),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_audit_householdstructuremember', null=True, to=orm['bcpp_household.HouseholdStructure'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', to=orm['bcpp_survey.Survey'])),
            ('internal_identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=36, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('age_in_years', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('lives_in_household', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('member_status', self.gf('django.db.models.fields.CharField')(default='NOT_REPORTED', max_length=25, null=True, db_index=True)),
            ('hiv_history', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('is_eligible_member', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contact_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructuremember', null=True, to=orm['bcpp_household.ContactLog'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureMemberAudit'])

        # Adding model 'HouseholdStructureMember'
        db.create_table('bcpp_household_householdstructuremember', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdStructure'], null=True, blank=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('internal_identifier', self.gf('django.db.models.fields.CharField')(default=None, max_length=36, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, db_index=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('age_in_years', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('lives_in_household', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('member_status', self.gf('django.db.models.fields.CharField')(default='NOT_REPORTED', max_length=25, null=True, db_index=True)),
            ('hiv_history', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('is_eligible_member', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('contact_log', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.ContactLog'], unique=True, null=True)),
            ('target', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureMember'])

        # Adding unique constraint on 'HouseholdStructureMember', fields ['household_structure', 'first_name', 'initials']
        db.create_unique('bcpp_household_householdstructuremember', ['household_structure_id', 'first_name', 'initials'])

        # Adding unique constraint on 'HouseholdStructureMember', fields ['registered_subject', 'household_structure']
        db.create_unique('bcpp_household_householdstructuremember', ['registered_subject_id', 'household_structure_id'])

        # Adding model 'HouseholdIdentifier'
        db.create_table('bcpp_household_householdidentifier', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('padding', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('sequence_number', self.gf('django.db.models.fields.IntegerField')()),
            ('device_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdIdentifier'])

        # Adding model 'HouseholdSurvey'
        db.create_table('bcpp_householdsurvey', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Household'])),
            ('survey_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.HouseholdSurveyCode'])),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdSurvey'])

        # Adding unique constraint on 'HouseholdSurvey', fields ['household', 'survey_code']
        db.create_unique('bcpp_householdsurvey', ['household_id', 'survey_code_id'])

        # Adding model 'HouseholdSurveyReport'
        db.create_table('bcpp_household_householdsurveyreport', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdSurvey'])),
            ('survey_date', self.gf('django.db.models.fields.DateField')()),
            ('survey_start_time', self.gf('django.db.models.fields.TimeField')()),
            ('survey_end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('household_survey_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.HouseholdSurveyStatus'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdSurveyReport'])

        # Adding unique constraint on 'HouseholdSurveyReport', fields ['household_survey', 'survey_date', 'survey_start_time']
        db.create_unique('bcpp_household_householdsurveyreport', ['household_survey_id', 'survey_date', 'survey_start_time'])

        # Adding model 'HouseholdLogAudit'
        db.create_table('bcpp_household_householdlog_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdlog', to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdlog', to=orm['bcpp_survey.Survey'])),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogAudit'])

        # Adding model 'HouseholdLog'
        db.create_table('bcpp_household_householdlog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLog'])

        # Adding unique constraint on 'HouseholdLog', fields ['household', 'survey']
        db.create_unique('bcpp_household_householdlog', ['household_id', 'survey_id'])

        # Adding model 'HouseholdLogEntryAudit'
        db.create_table('bcpp_household_householdlogentry_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('household_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdlogentry', to=orm['bcpp_household.HouseholdLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('hbc', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogEntryAudit'])

        # Adding model 'HouseholdLogEntry'
        db.create_table('bcpp_household_householdlogentry', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='melissa', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('hbc', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogEntry'])

        # Adding unique constraint on 'HouseholdLogEntry', fields ['household_log', 'report_datetime']
        db.create_unique('bcpp_household_householdlogentry', ['household_log_id', 'report_datetime'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'HouseholdLogEntry', fields ['household_log', 'report_datetime']
        db.delete_unique('bcpp_household_householdlogentry', ['household_log_id', 'report_datetime'])

        # Removing unique constraint on 'HouseholdLog', fields ['household', 'survey']
        db.delete_unique('bcpp_household_householdlog', ['household_id', 'survey_id'])

        # Removing unique constraint on 'HouseholdSurveyReport', fields ['household_survey', 'survey_date', 'survey_start_time']
        db.delete_unique('bcpp_household_householdsurveyreport', ['household_survey_id', 'survey_date', 'survey_start_time'])

        # Removing unique constraint on 'HouseholdSurvey', fields ['household', 'survey_code']
        db.delete_unique('bcpp_householdsurvey', ['household_id', 'survey_code_id'])

        # Removing unique constraint on 'HouseholdStructureMember', fields ['registered_subject', 'household_structure']
        db.delete_unique('bcpp_household_householdstructuremember', ['registered_subject_id', 'household_structure_id'])

        # Removing unique constraint on 'HouseholdStructureMember', fields ['household_structure', 'first_name', 'initials']
        db.delete_unique('bcpp_household_householdstructuremember', ['household_structure_id', 'first_name', 'initials'])

        # Removing unique constraint on 'HouseholdStructure', fields ['household', 'survey']
        db.delete_unique('bcpp_household_householdstructure', ['household_id', 'survey_id'])

        # Deleting model 'GpsDevice'
        db.delete_table('bcpp_household_gpsdevice')

        # Deleting model 'HouseholdAudit'
        db.delete_table('bcpp_household_household_audit')

        # Deleting model 'Household'
        db.delete_table('bcpp_household_household')

        # Removing M2M table for field ward on 'Household'
        db.delete_table('bcpp_household_household_ward')

        # Deleting model 'ContactLog'
        db.delete_table('bcpp_household_contactlog')

        # Deleting model 'ContactLogItem'
        db.delete_table('bcpp_household_contactlogitem')

        # Deleting model 'HouseholdStructureAudit'
        db.delete_table('bcpp_household_householdstructure_audit')

        # Deleting model 'HouseholdStructure'
        db.delete_table('bcpp_household_householdstructure')

        # Deleting model 'HouseholdStructureMemberAudit'
        db.delete_table('bcpp_household_householdstructuremember_audit')

        # Deleting model 'HouseholdStructureMember'
        db.delete_table('bcpp_household_householdstructuremember')

        # Deleting model 'HouseholdIdentifier'
        db.delete_table('bcpp_household_householdidentifier')

        # Deleting model 'HouseholdSurvey'
        db.delete_table('bcpp_householdsurvey')

        # Deleting model 'HouseholdSurveyReport'
        db.delete_table('bcpp_household_householdsurveyreport')

        # Deleting model 'HouseholdLogAudit'
        db.delete_table('bcpp_household_householdlog_audit')

        # Deleting model 'HouseholdLog'
        db.delete_table('bcpp_household_householdlog')

        # Deleting model 'HouseholdLogEntryAudit'
        db.delete_table('bcpp_household_householdlogentry_audit')

        # Deleting model 'HouseholdLogEntry'
        db.delete_table('bcpp_household_householdlogentry')


    models = {
        'bcpp_household.contactlog': {
            'Meta': {'object_name': 'ContactLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'gps_device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.GpsDevice']"}),
            'gps_point_1': ('django.db.models.fields.CharField', [], {'default': '24', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_11': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_point_2': ('django.db.models.fields.CharField', [], {'default': '26', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_21': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_waypoint': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'ward': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.BcppWards']", 'db_index': 'True', 'symmetrical': 'False'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'ward_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'was_surveyed_previously': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '10'})
        },
        'bcpp_household.householdidentifier': {
            'Meta': {'object_name': 'HouseholdIdentifier'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlog': {
            'Meta': {'unique_together': "(('household', 'survey'),)", 'object_name': 'HouseholdLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructuremember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdStructureMember'},
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.ContactLog']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'is_eligible_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lives_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructurememberaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdStructureMemberAudit', 'db_table': "'bcpp_household_householdstructuremember_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructuremember'", 'null': 'True', 'to': "orm['bcpp_household.ContactLog']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_audit_householdstructuremember'", 'null': 'True', 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'is_eligible_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lives_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructuremember'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructuremember'", 'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdsurvey': {
            'Meta': {'unique_together': "(('household', 'survey_code'),)", 'object_name': 'HouseholdSurvey', 'db_table': "'bcpp_householdsurvey'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.HouseholdSurveyCode']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdsurveyreport': {
            'Meta': {'ordering': "['-survey_date', 'survey_start_time']", 'unique_together': "(('household_survey', 'survey_date', 'survey_start_time'),)", 'object_name': 'HouseholdSurveyReport'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdSurvey']"}),
            'household_survey_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.HouseholdSurveyStatus']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_date': ('django.db.models.fields.DateField', [], {}),
            'survey_end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'survey_start_time': ('django.db.models.fields.TimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_list.bcppwards': {
            'Meta': {'object_name': 'BcppWards'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.householdsurveycode': {
            'Meta': {'object_name': 'HouseholdSurveyCode'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.householdsurveystatus': {
            'Meta': {'object_name': 'HouseholdSurveyStatus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.surveygroup': {
            'Meta': {'object_name': 'SurveyGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SurveyGroup']"}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('identity', 'first_name', 'dob', 'initials', 'registration_identifier'),)", 'object_name': 'RegisteredSubject'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bcpp_household']

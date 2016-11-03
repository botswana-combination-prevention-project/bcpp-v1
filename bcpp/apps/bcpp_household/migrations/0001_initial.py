# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Community'
        db.create_table(u'bcpp_household_community', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bcpp_household', ['Community'])

        # Adding model 'GpsDevice'
        db.create_table(u'bcpp_household_gpsdevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
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

        # Adding model 'PlotAudit'
        db.create_table(u'bcpp_household_plot_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('plot_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('eligible_members', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('cso_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=78L, null=True, blank=True)),
            ('household_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('time_of_week', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('time_of_day', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('gps_degrees_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_degrees_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lon', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lat', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_target_lon', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_target_lat', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('target_radius', self.gf('django.db.models.fields.FloatField')(default=0.025)),
            ('distance_from_target', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('selected', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='unconfirmed', max_length=25, null=True)),
            ('access_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uploaded_map_16', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('uploaded_map_17', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('uploaded_map_18', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('sub_section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('bhs', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('htc', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('replaces', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('replaced_by', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('replaceable', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['PlotAudit'])

        # Adding model 'Plot'
        db.create_table(u'bcpp_household_plot', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('plot_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, db_index=True)),
            ('eligible_members', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('cso_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=78L, null=True, blank=True)),
            ('household_count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('time_of_week', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('time_of_day', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('gps_degrees_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_degrees_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lon', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lat', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_target_lon', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_target_lat', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('target_radius', self.gf('django.db.models.fields.FloatField')(default=0.025)),
            ('distance_from_target', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('selected', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='unconfirmed', max_length=25, null=True)),
            ('access_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uploaded_map_16', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('uploaded_map_17', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('uploaded_map_18', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('sub_section', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('bhs', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('htc', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('replaces', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('replaced_by', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('replaceable', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['Plot'])

        # Adding unique constraint on 'Plot', fields ['gps_target_lat', 'gps_target_lon']
        db.create_unique(u'bcpp_household_plot', ['gps_target_lat', 'gps_target_lon'])

        # Adding model 'HouseholdAudit'
        db.create_table(u'bcpp_household_household_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('plot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_household', null=True, to=orm['bcpp_household.Plot'])),
            ('household_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('household_sequence', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('hh_int', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('hh_seed', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('gps_degrees_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_degrees_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_target_lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_target_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('target_radius', self.gf('django.db.models.fields.FloatField')(default=0.025)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('replaced_by', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('replaceable', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uploaded_map', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='unconfirmed', max_length=25, null=True)),
            ('enrolled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdAudit'])

        # Adding model 'Household'
        db.create_table(u'bcpp_household_household', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('plot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Plot'], null=True)),
            ('household_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True, null=True)),
            ('household_sequence', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('hh_int', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('hh_seed', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('gps_degrees_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_s', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_degrees_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_minutes_e', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('gps_lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_target_lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('gps_target_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('target_radius', self.gf('django.db.models.fields.FloatField')(default=0.025)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('replaced_by', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('replaceable', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('uploaded_map', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(default='unconfirmed', max_length=25, null=True)),
            ('enrolled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('bcpp_household', ['Household'])

        # Adding model 'HouseholdStructureAudit'
        db.create_table(u'bcpp_household_householdstructure_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructure', to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdstructure', to=orm['bcpp_survey.Survey'])),
            ('progress', self.gf('django.db.models.fields.CharField')(default='Not Started', max_length=25, null=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('enrolled', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('enrolled_household_member', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('enumerated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enumeration_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('refused_enumeration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('failed_enumeration_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('failed_enumeration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_informant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('eligible_members', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructureAudit'])

        # Adding model 'HouseholdStructure'
        db.create_table(u'bcpp_household_householdstructure', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.Household'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('progress', self.gf('django.db.models.fields.CharField')(default='Not Started', max_length=25, null=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('enrolled', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('enrolled_household_member', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('enrolled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('enumerated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enumeration_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('refused_enumeration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('failed_enumeration_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('failed_enumeration', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_informant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('eligible_members', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdStructure'])

        # Adding unique constraint on 'HouseholdStructure', fields ['survey', 'household']
        db.create_unique(u'bcpp_household_householdstructure', ['survey_id', 'household_id'])

        # Adding model 'HouseholdAssessmentAudit'
        db.create_table(u'bcpp_household_householdassessment_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('residency', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('eligibles', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('ineligible_reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_seen_home', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdassessment', to=orm['bcpp_household.HouseholdStructure'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdAssessmentAudit'])

        # Adding model 'HouseholdAssessment'
        db.create_table(u'bcpp_household_householdassessment', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
            ('residency', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('eligibles', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('ineligible_reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_seen_home', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdAssessment'])

        # Adding model 'HouseholdRefusalAudit'
        db.create_table(u'bcpp_household_householdrefusal_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdrefusal', to=orm['bcpp_household.HouseholdStructure'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdRefusalAudit'])

        # Adding model 'HouseholdRefusal'
        db.create_table(u'bcpp_household_householdrefusal', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdRefusal'])

        # Adding model 'HouseholdRefusalHistoryAudit'
        db.create_table(u'bcpp_household_householdrefusalhistory_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('transaction', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdrefusalhistory', to=orm['bcpp_household.HouseholdStructure'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdRefusalHistoryAudit'])

        # Adding model 'HouseholdRefusalHistory'
        db.create_table(u'bcpp_household_householdrefusalhistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('transaction', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdRefusalHistory'])

        # Adding model 'HouseholdIdentifierHistory'
        db.create_table(u'bcpp_household_householdidentifierhistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('padding', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('sequence_number', self.gf('django.db.models.fields.IntegerField')()),
            ('device_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_derived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sequence_app_label', self.gf('django.db.models.fields.CharField')(default='bhp_identifier', max_length=50)),
            ('sequence_model_name', self.gf('django.db.models.fields.CharField')(default='sequence', max_length=50)),
            ('plot_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('household_sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdIdentifierHistory'])

        # Adding model 'HouseholdLogAudit'
        db.create_table(u'bcpp_household_householdlog_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdlog', to=orm['bcpp_household.HouseholdStructure'])),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogAudit'])

        # Adding model 'HouseholdLog'
        db.create_table(u'bcpp_household_householdlog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLog'])

        # Adding model 'HouseholdLogEntryAudit'
        db.create_table(u'bcpp_household_householdlogentry_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('household_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdlogentry', to=orm['bcpp_household.HouseholdLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateField')()),
            ('household_status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogEntryAudit'])

        # Adding model 'HouseholdLogEntry'
        db.create_table(u'bcpp_household_householdlogentry', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('household_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.HouseholdLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateField')()),
            ('household_status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['HouseholdLogEntry'])

        # Adding unique constraint on 'HouseholdLogEntry', fields ['household_log', 'report_datetime']
        db.create_unique(u'bcpp_household_householdlogentry', ['household_log_id', 'report_datetime'])

        # Adding model 'PlotIdentifierHistory'
        db.create_table(u'bcpp_household_plotidentifierhistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('padding', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('sequence_number', self.gf('django.db.models.fields.IntegerField')()),
            ('device_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_derived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sequence_app_label', self.gf('django.db.models.fields.CharField')(default='bhp_identifier', max_length=50)),
            ('sequence_model_name', self.gf('django.db.models.fields.CharField')(default='sequence', max_length=50)),
        ))
        db.send_create_signal('bcpp_household', ['PlotIdentifierHistory'])

        # Adding model 'PlotLogAudit'
        db.create_table(u'bcpp_household_plotlog_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('plot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_plotlog', to=orm['bcpp_household.Plot'])),
        ))
        db.send_create_signal('bcpp_household', ['PlotLogAudit'])

        # Adding model 'PlotLog'
        db.create_table(u'bcpp_household_plotlog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('plot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.Plot'], unique=True)),
        ))
        db.send_create_signal('bcpp_household', ['PlotLog'])

        # Adding model 'PlotLogEntryAudit'
        db.create_table(u'bcpp_household_plotlogentry_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('plot_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_plotlogentry', to=orm['bcpp_household.PlotLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('log_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['PlotLogEntryAudit'])

        # Adding model 'PlotLogEntry'
        db.create_table(u'bcpp_household_plotlogentry', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('plot_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.PlotLog'])),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('log_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_household', ['PlotLogEntry'])

        # Adding unique constraint on 'PlotLogEntry', fields ['plot_log', 'report_datetime']
        db.create_unique(u'bcpp_household_plotlogentry', ['plot_log_id', 'report_datetime'])

        # Adding model 'Replaceable'
        db.create_table(u'bcpp_household_replaceable', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('replaced', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('replaced_reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('producer_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('plot_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('item_pk', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('item_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_household', ['Replaceable'])

        # Adding model 'ReplacementHistoryAudit'
        db.create_table(u'bcpp_household_replacementhistory_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('replacing_item', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('replaced_item', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('replacement_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('replacement_reason', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_household', ['ReplacementHistoryAudit'])

        # Adding model 'ReplacementHistory'
        db.create_table(u'bcpp_household_replacementhistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('replacing_item', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('replaced_item', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('replacement_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('replacement_reason', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('bcpp_household', ['ReplacementHistory'])

        # Adding unique constraint on 'ReplacementHistory', fields ['replacing_item', 'replaced_item']
        db.create_unique(u'bcpp_household_replacementhistory', ['replacing_item', 'replaced_item'])

        # Adding model 'IncreasePlotRadiusAudit'
        db.create_table(u'bcpp_household_increaseplotradius_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(default=25.0)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('plot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_increaseplotradius', to=orm['bcpp_household.Plot'])),
        ))
        db.send_create_signal('bcpp_household', ['IncreasePlotRadiusAudit'])

        # Adding model 'IncreasePlotRadius'
        db.create_table(u'bcpp_household_increaseplotradius', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('plot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.Plot'], unique=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(default=25.0)),
        ))
        db.send_create_signal('bcpp_household', ['IncreasePlotRadius'])

        # Adding model 'RepresentativeEligibilityAudit'
        db.create_table(u'bcpp_household_representativeeligibility_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('aged_over_18', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('household_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('verbal_script', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_representativeeligibility', to=orm['bcpp_household.HouseholdStructure'])),
        ))
        db.send_create_signal('bcpp_household', ['RepresentativeEligibilityAudit'])

        # Adding model 'RepresentativeEligibility'
        db.create_table(u'bcpp_household_representativeeligibility', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('aged_over_18', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('household_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('verbal_script', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
        ))
        db.send_create_signal('bcpp_household', ['RepresentativeEligibility'])


    def backwards(self, orm):
        # Removing unique constraint on 'ReplacementHistory', fields ['replacing_item', 'replaced_item']
        db.delete_unique(u'bcpp_household_replacementhistory', ['replacing_item', 'replaced_item'])

        # Removing unique constraint on 'PlotLogEntry', fields ['plot_log', 'report_datetime']
        db.delete_unique(u'bcpp_household_plotlogentry', ['plot_log_id', 'report_datetime'])

        # Removing unique constraint on 'HouseholdLogEntry', fields ['household_log', 'report_datetime']
        db.delete_unique(u'bcpp_household_householdlogentry', ['household_log_id', 'report_datetime'])

        # Removing unique constraint on 'HouseholdStructure', fields ['survey', 'household']
        db.delete_unique(u'bcpp_household_householdstructure', ['survey_id', 'household_id'])

        # Removing unique constraint on 'Plot', fields ['gps_target_lat', 'gps_target_lon']
        db.delete_unique(u'bcpp_household_plot', ['gps_target_lat', 'gps_target_lon'])

        # Deleting model 'Community'
        db.delete_table(u'bcpp_household_community')

        # Deleting model 'GpsDevice'
        db.delete_table(u'bcpp_household_gpsdevice')

        # Deleting model 'PlotAudit'
        db.delete_table(u'bcpp_household_plot_audit')

        # Deleting model 'Plot'
        db.delete_table(u'bcpp_household_plot')

        # Deleting model 'HouseholdAudit'
        db.delete_table(u'bcpp_household_household_audit')

        # Deleting model 'Household'
        db.delete_table(u'bcpp_household_household')

        # Deleting model 'HouseholdStructureAudit'
        db.delete_table(u'bcpp_household_householdstructure_audit')

        # Deleting model 'HouseholdStructure'
        db.delete_table(u'bcpp_household_householdstructure')

        # Deleting model 'HouseholdAssessmentAudit'
        db.delete_table(u'bcpp_household_householdassessment_audit')

        # Deleting model 'HouseholdAssessment'
        db.delete_table(u'bcpp_household_householdassessment')

        # Deleting model 'HouseholdRefusalAudit'
        db.delete_table(u'bcpp_household_householdrefusal_audit')

        # Deleting model 'HouseholdRefusal'
        db.delete_table(u'bcpp_household_householdrefusal')

        # Deleting model 'HouseholdRefusalHistoryAudit'
        db.delete_table(u'bcpp_household_householdrefusalhistory_audit')

        # Deleting model 'HouseholdRefusalHistory'
        db.delete_table(u'bcpp_household_householdrefusalhistory')

        # Deleting model 'HouseholdIdentifierHistory'
        db.delete_table(u'bcpp_household_householdidentifierhistory')

        # Deleting model 'HouseholdLogAudit'
        db.delete_table(u'bcpp_household_householdlog_audit')

        # Deleting model 'HouseholdLog'
        db.delete_table(u'bcpp_household_householdlog')

        # Deleting model 'HouseholdLogEntryAudit'
        db.delete_table(u'bcpp_household_householdlogentry_audit')

        # Deleting model 'HouseholdLogEntry'
        db.delete_table(u'bcpp_household_householdlogentry')

        # Deleting model 'PlotIdentifierHistory'
        db.delete_table(u'bcpp_household_plotidentifierhistory')

        # Deleting model 'PlotLogAudit'
        db.delete_table(u'bcpp_household_plotlog_audit')

        # Deleting model 'PlotLog'
        db.delete_table(u'bcpp_household_plotlog')

        # Deleting model 'PlotLogEntryAudit'
        db.delete_table(u'bcpp_household_plotlogentry_audit')

        # Deleting model 'PlotLogEntry'
        db.delete_table(u'bcpp_household_plotlogentry')

        # Deleting model 'Replaceable'
        db.delete_table(u'bcpp_household_replaceable')

        # Deleting model 'ReplacementHistoryAudit'
        db.delete_table(u'bcpp_household_replacementhistory_audit')

        # Deleting model 'ReplacementHistory'
        db.delete_table(u'bcpp_household_replacementhistory')

        # Deleting model 'IncreasePlotRadiusAudit'
        db.delete_table(u'bcpp_household_increaseplotradius_audit')

        # Deleting model 'IncreasePlotRadius'
        db.delete_table(u'bcpp_household_increaseplotradius')

        # Deleting model 'RepresentativeEligibilityAudit'
        db.delete_table(u'bcpp_household_representativeeligibility_audit')

        # Deleting model 'RepresentativeEligibility'
        db.delete_table(u'bcpp_household_representativeeligibility')


    models = {
        'bcpp_household.community': {
            'Meta': {'object_name': 'Community'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
            'replaceable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'replaced_by': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdassessment': {
            'Meta': {'object_name': 'HouseholdAssessment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligibles': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'ineligible_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_seen_home': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'residency': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdassessmentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdAssessmentAudit', 'db_table': "u'bcpp_household_householdassessment_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligibles': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdassessment'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'ineligible_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_seen_home': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'residency': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdAudit', 'db_table': "u'bcpp_household_household_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_household'", 'null': 'True', 'to': "orm['bcpp_household.Plot']"}),
            'replaceable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'replaced_by': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdidentifierhistory': {
            'Meta': {'object_name': 'HouseholdIdentifierHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'is_derived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sequence_app_label': ('django.db.models.fields.CharField', [], {'default': "'bhp_identifier'", 'max_length': '50'}),
            'sequence_model_name': ('django.db.models.fields.CharField', [], {'default': "'sequence'", 'max_length': '50'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlog': {
            'Meta': {'object_name': 'HouseholdLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdLogAudit', 'db_table': "u'bcpp_household_householdlog_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdlog'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogentry': {
            'Meta': {'unique_together': "(('household_log', 'report_datetime'),)", 'object_name': 'HouseholdLogEntry'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdLog']"}),
            'household_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdlogentryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdLogEntryAudit', 'db_table': "u'bcpp_household_householdlogentry_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdlogentry'", 'to': "orm['bcpp_household.HouseholdLog']"}),
            'household_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdrefusal': {
            'Meta': {'ordering': "['household_structure']", 'object_name': 'HouseholdRefusal'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdrefusalaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdRefusalAudit', 'db_table': "u'bcpp_household_householdrefusal_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdrefusal'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdrefusalhistory': {
            'Meta': {'ordering': "['household_structure']", 'object_name': 'HouseholdRefusalHistory'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdrefusalhistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdRefusalHistoryAudit', 'db_table': "u'bcpp_household_householdrefusalhistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdrefusalhistory'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructure': {
            'Meta': {'unique_together': "(('survey', 'household'),)", 'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligible_members': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enrolled': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'enrolled_household_member': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'enumerated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'failed_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'failed_enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_informant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'Not Started'", 'max_length': '25', 'null': 'True'}),
            'refused_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructureaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdStructureAudit', 'db_table': "u'bcpp_household_householdstructure_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligible_members': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enrolled': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'enrolled_household_member': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'enumerated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'failed_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'failed_enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_informant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'Not Started'", 'max_length': '25', 'null': 'True'}),
            'refused_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdstructure'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.increaseplotradius': {
            'Meta': {'object_name': 'IncreasePlotRadius'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.Plot']", 'unique': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.increaseplotradiusaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'IncreasePlotRadiusAudit', 'db_table': "u'bcpp_household_increaseplotradius_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_increaseplotradius'", 'to': "orm['bcpp_household.Plot']"}),
            'radius': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plot': {
            'Meta': {'ordering': "['-plot_identifier']", 'unique_together': "(('gps_target_lat', 'gps_target_lon'),)", 'object_name': 'Plot'},
            'access_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'bhs': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'distance_from_target': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'htc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'replaceable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'replaced_by': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'replaces': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'sub_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'time_of_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'time_of_week': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_16': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_17': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_18': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PlotAudit', 'db_table': "u'bcpp_household_plot_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'access_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'bhs': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'distance_from_target': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'htc': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'replaceable': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'replaced_by': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'replaces': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'selected': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'sub_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'time_of_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'time_of_week': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_16': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_17': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'uploaded_map_18': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotidentifierhistory': {
            'Meta': {'object_name': 'PlotIdentifierHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'is_derived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sequence_app_label': ('django.db.models.fields.CharField', [], {'default': "'bhp_identifier'", 'max_length': '50'}),
            'sequence_model_name': ('django.db.models.fields.CharField', [], {'default': "'sequence'", 'max_length': '50'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotlog': {
            'Meta': {'object_name': 'PlotLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.Plot']", 'unique': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotlogaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PlotLogAudit', 'db_table': "u'bcpp_household_plotlog_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_plotlog'", 'to': "orm['bcpp_household.Plot']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotlogentry': {
            'Meta': {'unique_together': "(('plot_log', 'report_datetime'),)", 'object_name': 'PlotLogEntry'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'log_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.PlotLog']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plotlogentryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PlotLogEntryAudit', 'db_table': "u'bcpp_household_plotlogentry_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'log_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_plotlogentry'", 'to': "orm['bcpp_household.PlotLog']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.replaceable': {
            'Meta': {'object_name': 'Replaceable'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'item_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'producer_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'replaced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'replaced_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.replacementhistory': {
            'Meta': {'ordering': "['-replacing_item']", 'unique_together': "(('replacing_item', 'replaced_item'),)", 'object_name': 'ReplacementHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'replaced_item': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'replacement_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'replacement_reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'replacing_item': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.replacementhistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReplacementHistoryAudit', 'db_table': "u'bcpp_household_replacementhistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'replaced_item': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'replacement_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'replacement_reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'replacing_item': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.representativeeligibility': {
            'Meta': {'object_name': 'RepresentativeEligibility'},
            'aged_over_18': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_script': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'bcpp_household.representativeeligibilityaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'RepresentativeEligibilityAudit', 'db_table': "u'bcpp_household_representativeeligibility_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aged_over_18': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_representativeeligibility'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_script': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'bcpp_survey.survey': {
            'Meta': {'ordering': "['survey_name']", 'object_name': 'Survey'},
            'chronological_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bcpp_household']
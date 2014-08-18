# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RepresentativeEligibilityAudit'
#         db.create_table(u'bcpp_household_representativeeligibility_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('aged_over_18', self.gf('django.db.models.fields.CharField')(max_length=10)),
#             ('household_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
#             ('verbal_script', self.gf('django.db.models.fields.CharField')(max_length=10)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_representativeeligibility', to=orm['bcpp_household.HouseholdStructure'])),
#         ))
#         db.send_create_signal('bcpp_household', ['RepresentativeEligibilityAudit'])

        # Adding model 'ReplacementHistory'
#         db.create_table(u'bcpp_household_replacementhistory', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('replacing_item', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('replaced_item', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('replacement_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
#             ('replacement_reason', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['ReplacementHistory'])

        # Adding unique constraint on 'ReplacementHistory', fields ['replacing_item', 'replaced_item']
#         db.create_unique(u'bcpp_household_replacementhistory', ['replacing_item', 'replaced_item'])

        # Adding model 'HouseholdRefusal'
#         db.create_table(u'bcpp_household_householdrefusal', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
#             ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdRefusal'])

        # Adding model 'HouseholdRefusalAudit'
#         db.create_table(u'bcpp_household_householdrefusal_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
#             ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdrefusal', to=orm['bcpp_household.HouseholdStructure'])),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdRefusalAudit'])

        # Adding model 'HouseholdAssessmentAudit'
#         db.create_table(u'bcpp_household_householdassessment_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('residency', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
#             ('eligibles', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('ineligible_reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('last_seen_home', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdassessment', to=orm['bcpp_household.HouseholdStructure'])),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdAssessmentAudit'])

        # Adding model 'PlotLogEntryAudit'
#         db.create_table(u'bcpp_household_plotlogentry_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('plot_log', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_plotlogentry', to=orm['bcpp_household.PlotLog'])),
#             ('log_status', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['PlotLogEntryAudit'])

        # Adding model 'RepresentativeEligibility'
#         db.create_table(u'bcpp_household_representativeeligibility', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('aged_over_18', self.gf('django.db.models.fields.CharField')(max_length=10)),
#             ('household_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
#             ('verbal_script', self.gf('django.db.models.fields.CharField')(max_length=10)),
#             ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['RepresentativeEligibility'])

        # Adding model 'ReplacementHistoryAudit'
#         db.create_table(u'bcpp_household_replacementhistory_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('replacing_item', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('replaced_item', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('replacement_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
#             ('replacement_reason', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['ReplacementHistoryAudit'])

        # Adding model 'PlotLogEntry'
#         db.create_table(u'bcpp_household_plotlogentry', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('plot_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_household.PlotLog'])),
#             ('log_status', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['PlotLogEntry'])

        # Adding unique constraint on 'PlotLogEntry', fields ['plot_log', 'report_datetime']
#         db.create_unique(u'bcpp_household_plotlogentry', ['plot_log_id', 'report_datetime'])

        # Adding model 'HouseholdAssessment'
#         db.create_table(u'bcpp_household_householdassessment', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
#             ('residency', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
#             ('member_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
#             ('eligibles', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('ineligible_reason', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#             ('last_seen_home', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdAssessment'])

        # Adding model 'PlotLogAudit'
#         db.create_table(u'bcpp_household_plotlog_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('plot', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_plotlog', to=orm['bcpp_household.Plot'])),
#         ))
#         db.send_create_signal('bcpp_household', ['PlotLogAudit'])

        # Adding model 'HouseholdRefusalHistory'
#         db.create_table(u'bcpp_household_householdrefusalhistory', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.HouseholdStructure'], unique=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
#             ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#             ('transaction', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdRefusalHistory'])

        # Adding model 'PlotLog'
#         db.create_table(u'bcpp_household_plotlog', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('plot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household.Plot'], unique=True)),
#         ))
#         db.send_create_signal('bcpp_household', ['PlotLog'])

        # Adding model 'HouseholdRefusalHistoryAudit'
#         db.create_table(u'bcpp_household_householdrefusalhistory_audit', (
#             ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
#             ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
#             ('hostname_created', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='One.local', max_length=50, db_index=True, blank=True)),
#             ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
#             ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
#             ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
#             ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
#             ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
#             ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
#             ('transaction', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
#             ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
#             ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
#             ('id', self.gf('django.db.models.fields.CharField')(max_length=36)),
#             ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
#             ('household_structure', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdrefusalhistory', to=orm['bcpp_household.HouseholdStructure'])),
#         ))
#         db.send_create_signal('bcpp_household', ['HouseholdRefusalHistoryAudit'])


        # Changing field 'HouseholdLog.revision'
        #db.alter_column(u'bcpp_household_householdlog', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
        # Deleting field 'HouseholdLogEntry.status'
        #db.delete_column(u'bcpp_household_householdlogentry', 'status')

        # Adding field 'HouseholdLogEntry.household_status'
        #db.add_column(u'bcpp_household_householdlogentry', 'household_status',
        #              self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
        #              keep_default=False)


        # Changing field 'HouseholdLogEntry.report_datetime'
        #db.alter_column(u'bcpp_household_householdlogentry', 'report_datetime', self.gf('django.db.models.fields.DateField')())

        # Changing field 'HouseholdLogEntry.revision'
#         db.alter_column(u'bcpp_household_householdlogentry', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Deleting field 'HouseholdStructure.member_count'
#         db.delete_column(u'bcpp_household_householdstructure', 'member_count')
# 
#         # Adding field 'HouseholdStructure.enrolled'
#         db.add_column(u'bcpp_household_householdstructure', 'enrolled',
#                       self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.enrolled_household_member'
#         db.add_column(u'bcpp_household_householdstructure', 'enrolled_household_member',
#                       self.gf('django.db.models.fields.CharField')(max_length=36, null=True),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.enrolled_datetime'
#         db.add_column(u'bcpp_household_householdstructure', 'enrolled_datetime',
#                       self.gf('django.db.models.fields.DateTimeField')(null=True),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.enumerated'
#         db.add_column(u'bcpp_household_householdstructure', 'enumerated',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.enumeration_attempts'
#         db.add_column(u'bcpp_household_householdstructure', 'enumeration_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.refused_enumeration'
#         db.add_column(u'bcpp_household_householdstructure', 'refused_enumeration',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.failed_enumeration_attempts'
#         db.add_column(u'bcpp_household_householdstructure', 'failed_enumeration_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.failed_enumeration'
#         db.add_column(u'bcpp_household_householdstructure', 'failed_enumeration',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.no_informant'
#         db.add_column(u'bcpp_household_householdstructure', 'no_informant',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)
# 
#         # Adding field 'HouseholdStructure.eligible_members'
#         db.add_column(u'bcpp_household_householdstructure', 'eligible_members',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)
# 
# 
#         # Changing field 'HouseholdStructure.revision'
#         db.alter_column(u'bcpp_household_householdstructure', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Deleting field 'HouseholdLogEntryAudit.status'
#         db.delete_column(u'bcpp_household_householdlogentry_audit', 'status')
# 
#         # Adding field 'HouseholdLogEntryAudit._audit_subject_identifier'
#         db.add_column(u'bcpp_household_householdlogentry_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdLogEntryAudit.household_status'
#         db.add_column(u'bcpp_household_householdlogentry_audit', 'household_status',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)


        # Changing field 'HouseholdLogEntryAudit.report_datetime'
#         db.alter_column(u'bcpp_household_householdlogentry_audit', 'report_datetime', self.gf('django.db.models.fields.DateField')())
# 
#         # Changing field 'HouseholdLogEntryAudit.revision'
#         db.alter_column(u'bcpp_household_householdlogentry_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Adding field 'Plot.comment'
#         db.add_column(u'bcpp_household_plot', 'comment',
#                       self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
#                       keep_default=False)

        # Adding field 'Plot.distance_from_target'
#         db.add_column(u'bcpp_household_plot', 'distance_from_target',
#                       self.gf('django.db.models.fields.FloatField')(null=True),
#                       keep_default=False)

        # Adding field 'Plot.replaces'
#         db.add_column(u'bcpp_household_plot', 'replaces',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
#                       keep_default=False)

        # Adding field 'Plot.access_attempts'
#         db.add_column(u'bcpp_household_plot', 'access_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)

        # Adding field 'Plot.bhs'
#         db.add_column(u'bcpp_household_plot', 'bhs',
#                       self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
#                       keep_default=False)

        # Adding field 'Plot.replaced_by'
#         db.add_column(u'bcpp_household_plot', 'replaced_by',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
#                       keep_default=False)


        # Changing field 'Plot.revision'
#         db.alter_column(u'bcpp_household_plot', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
# 
#         # Changing field 'Plot.status'
#         db.alter_column(u'bcpp_household_plot', 'status', self.gf('django.db.models.fields.CharField')(max_length=35, null=True))
# 
#         # Changing field 'Plot.uploaded_map_18'
#         db.alter_column(u'bcpp_household_plot', 'uploaded_map_18', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))
# 
#         # Changing field 'Plot.uploaded_map_17'
#         db.alter_column(u'bcpp_household_plot', 'uploaded_map_17', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))
# 
#         # Changing field 'Plot.uploaded_map_16'
#         db.alter_column(u'bcpp_household_plot', 'uploaded_map_16', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))
# 
#         # Changing field 'PlotIdentifierHistory.revision'
#         db.alter_column(u'bcpp_household_plotidentifierhistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Deleting field 'HouseholdStructureAudit.member_count'
#         db.delete_column(u'bcpp_household_householdstructure_audit', 'member_count')

        # Adding field 'HouseholdStructureAudit._audit_subject_identifier'
#         db.add_column(u'bcpp_household_householdstructure_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.enrolled'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'enrolled',
#                       self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.enrolled_household_member'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'enrolled_household_member',
#                       self.gf('django.db.models.fields.CharField')(max_length=36, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.enrolled_datetime'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'enrolled_datetime',
#                       self.gf('django.db.models.fields.DateTimeField')(null=True),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.enumerated'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'enumerated',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.enumeration_attempts'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'enumeration_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.refused_enumeration'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'refused_enumeration',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.failed_enumeration_attempts'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'failed_enumeration_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.failed_enumeration'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'failed_enumeration',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.no_informant'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'no_informant',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'HouseholdStructureAudit.eligible_members'
#         db.add_column(u'bcpp_household_householdstructure_audit', 'eligible_members',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)


        # Changing field 'HouseholdStructureAudit.revision'
#         db.alter_column(u'bcpp_household_householdstructure_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Adding field 'HouseholdAudit._audit_subject_identifier'
#         db.add_column(u'bcpp_household_household_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdAudit.replaced_by'
#         db.add_column(u'bcpp_household_household_audit', 'replaced_by',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdAudit.enrolled'
#         db.add_column(u'bcpp_household_household_audit', 'enrolled',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'HouseholdAudit.complete'
#         db.add_column(u'bcpp_household_household_audit', 'complete',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)


        # Changing field 'HouseholdAudit.revision'
#         db.alter_column(u'bcpp_household_household_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
# 
#         # Changing field 'HouseholdIdentifierHistory.revision'
#         db.alter_column(u'bcpp_household_householdidentifierhistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Adding field 'HouseholdLogAudit._audit_subject_identifier'
#         db.add_column(u'bcpp_household_householdlog_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)


        # Changing field 'HouseholdLogAudit.revision'
#         db.alter_column(u'bcpp_household_householdlog_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Adding field 'Household.replaced_by'
#         db.add_column(u'bcpp_household_household', 'replaced_by',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True),
#                       keep_default=False)

        # Adding field 'Household.enrolled'
#         db.add_column(u'bcpp_household_household', 'enrolled',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)

        # Adding field 'Household.complete'
#         db.add_column(u'bcpp_household_household', 'complete',
#                       self.gf('django.db.models.fields.BooleanField')(default=False),
#                       keep_default=False)


        # Changing field 'Household.revision'
#         db.alter_column(u'bcpp_household_household', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
#         # Adding field 'PlotAudit._audit_subject_identifier'
#         db.add_column(u'bcpp_household_plot_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

        # Adding field 'PlotAudit.comment'
#         db.add_column(u'bcpp_household_plot_audit', 'comment',
#                       self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
#                       keep_default=False)

        # Adding field 'PlotAudit.distance_from_target'
#         db.add_column(u'bcpp_household_plot_audit', 'distance_from_target',
#                       self.gf('django.db.models.fields.FloatField')(null=True),
#                       keep_default=False)

        # Adding field 'PlotAudit.replaces'
#         db.add_column(u'bcpp_household_plot_audit', 'replaces',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
#                       keep_default=False)

        # Adding field 'PlotAudit.access_attempts'
#         db.add_column(u'bcpp_household_plot_audit', 'access_attempts',
#                       self.gf('django.db.models.fields.IntegerField')(default=0),
#                       keep_default=False)

        # Adding field 'PlotAudit.bhs'
#         db.add_column(u'bcpp_household_plot_audit', 'bhs',
#                       self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
#                       keep_default=False)

        # Adding field 'PlotAudit.replaced_by'
#         db.add_column(u'bcpp_household_plot_audit', 'replaced_by',
#                       self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
#                       keep_default=False)


        # Changing field 'PlotAudit.revision'
        db.alter_column(u'bcpp_household_plot_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'PlotAudit.status'
        db.alter_column(u'bcpp_household_plot_audit', 'status', self.gf('django.db.models.fields.CharField')(max_length=35, null=True))

        # Changing field 'PlotAudit.uploaded_map_18'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_18', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'PlotAudit.uploaded_map_17'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_17', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

        # Changing field 'PlotAudit.uploaded_map_16'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_16', self.gf('django.db.models.fields.CharField')(max_length=25, null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'PlotLogEntry', fields ['plot_log', 'report_datetime']
        db.delete_unique(u'bcpp_household_plotlogentry', ['plot_log_id', 'report_datetime'])

        # Removing unique constraint on 'ReplacementHistory', fields ['replacing_item', 'replaced_item']
        db.delete_unique(u'bcpp_household_replacementhistory', ['replacing_item', 'replaced_item'])

        # Deleting model 'RepresentativeEligibilityAudit'
        db.delete_table(u'bcpp_household_representativeeligibility_audit')

        # Deleting model 'ReplacementHistory'
        db.delete_table(u'bcpp_household_replacementhistory')

        # Deleting model 'HouseholdRefusal'
        db.delete_table(u'bcpp_household_householdrefusal')

        # Deleting model 'HouseholdRefusalAudit'
        db.delete_table(u'bcpp_household_householdrefusal_audit')

        # Deleting model 'HouseholdAssessmentAudit'
        db.delete_table(u'bcpp_household_householdassessment_audit')

        # Deleting model 'PlotLogEntryAudit'
        db.delete_table(u'bcpp_household_plotlogentry_audit')

        # Deleting model 'RepresentativeEligibility'
        db.delete_table(u'bcpp_household_representativeeligibility')

        # Deleting model 'ReplacementHistoryAudit'
        db.delete_table(u'bcpp_household_replacementhistory_audit')

        # Deleting model 'PlotLogEntry'
        db.delete_table(u'bcpp_household_plotlogentry')

        # Deleting model 'HouseholdAssessment'
        db.delete_table(u'bcpp_household_householdassessment')

        # Deleting model 'PlotLogAudit'
        db.delete_table(u'bcpp_household_plotlog_audit')

        # Deleting model 'HouseholdRefusalHistory'
        db.delete_table(u'bcpp_household_householdrefusalhistory')

        # Deleting model 'PlotLog'
        db.delete_table(u'bcpp_household_plotlog')

        # Deleting model 'HouseholdRefusalHistoryAudit'
        db.delete_table(u'bcpp_household_householdrefusalhistory_audit')


        # Changing field 'HouseholdLog.revision'
        db.alter_column(u'bcpp_household_householdlog', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Adding field 'HouseholdLogEntry.status'
        db.add_column(u'bcpp_household_householdlogentry', 'status',
                      self.gf('django.db.models.fields.CharField')(default='occupied', max_length=25),
                      keep_default=False)

        # Deleting field 'HouseholdLogEntry.household_status'
        db.delete_column(u'bcpp_household_householdlogentry', 'household_status')


        # Changing field 'HouseholdLogEntry.report_datetime'
        db.alter_column(u'bcpp_household_householdlogentry', 'report_datetime', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HouseholdLogEntry.revision'
        db.alter_column(u'bcpp_household_householdlogentry', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Adding field 'HouseholdStructure.member_count'
        db.add_column(u'bcpp_household_householdstructure', 'member_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'HouseholdStructure.enrolled'
        db.delete_column(u'bcpp_household_householdstructure', 'enrolled')

        # Deleting field 'HouseholdStructure.enrolled_household_member'
        db.delete_column(u'bcpp_household_householdstructure', 'enrolled_household_member')

        # Deleting field 'HouseholdStructure.enrolled_datetime'
        db.delete_column(u'bcpp_household_householdstructure', 'enrolled_datetime')

        # Deleting field 'HouseholdStructure.enumerated'
        db.delete_column(u'bcpp_household_householdstructure', 'enumerated')

        # Deleting field 'HouseholdStructure.enumeration_attempts'
        db.delete_column(u'bcpp_household_householdstructure', 'enumeration_attempts')

        # Deleting field 'HouseholdStructure.refused_enumeration'
        db.delete_column(u'bcpp_household_householdstructure', 'refused_enumeration')

        # Deleting field 'HouseholdStructure.failed_enumeration_attempts'
        db.delete_column(u'bcpp_household_householdstructure', 'failed_enumeration_attempts')

        # Deleting field 'HouseholdStructure.failed_enumeration'
        db.delete_column(u'bcpp_household_householdstructure', 'failed_enumeration')

        # Deleting field 'HouseholdStructure.no_informant'
        db.delete_column(u'bcpp_household_householdstructure', 'no_informant')

        # Deleting field 'HouseholdStructure.eligible_members'
        db.delete_column(u'bcpp_household_householdstructure', 'eligible_members')


        # Changing field 'HouseholdStructure.revision'
        db.alter_column(u'bcpp_household_householdstructure', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Adding field 'HouseholdLogEntryAudit.status'
        db.add_column(u'bcpp_household_householdlogentry_audit', 'status',
                      self.gf('django.db.models.fields.CharField')(default='occupied', max_length=25),
                      keep_default=False)

        # Deleting field 'HouseholdLogEntryAudit._audit_subject_identifier'
        db.delete_column(u'bcpp_household_householdlogentry_audit', '_audit_subject_identifier')

        # Deleting field 'HouseholdLogEntryAudit.household_status'
        db.delete_column(u'bcpp_household_householdlogentry_audit', 'household_status')


        # Changing field 'HouseholdLogEntryAudit.report_datetime'
        db.alter_column(u'bcpp_household_householdlogentry_audit', 'report_datetime', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HouseholdLogEntryAudit.revision'
        db.alter_column(u'bcpp_household_householdlogentry_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Deleting field 'Plot.comment'
        db.delete_column(u'bcpp_household_plot', 'comment')

        # Deleting field 'Plot.distance_from_target'
        db.delete_column(u'bcpp_household_plot', 'distance_from_target')

        # Deleting field 'Plot.replaces'
        db.delete_column(u'bcpp_household_plot', 'replaces')

        # Deleting field 'Plot.access_attempts'
        db.delete_column(u'bcpp_household_plot', 'access_attempts')

        # Deleting field 'Plot.bhs'
        db.delete_column(u'bcpp_household_plot', 'bhs')

        # Deleting field 'Plot.replaced_by'
        db.delete_column(u'bcpp_household_plot', 'replaced_by')


        # Changing field 'Plot.revision'
        db.alter_column(u'bcpp_household_plot', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Plot.status'
        db.alter_column(u'bcpp_household_plot', 'status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Plot.uploaded_map_18'
        db.alter_column(u'bcpp_household_plot', 'uploaded_map_18', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Plot.uploaded_map_17'
        db.alter_column(u'bcpp_household_plot', 'uploaded_map_17', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Plot.uploaded_map_16'
        db.alter_column(u'bcpp_household_plot', 'uploaded_map_16', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'PlotIdentifierHistory.revision'
        db.alter_column(u'bcpp_household_plotidentifierhistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Adding field 'HouseholdStructureAudit.member_count'
        db.add_column(u'bcpp_household_householdstructure_audit', 'member_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'HouseholdStructureAudit._audit_subject_identifier'
        db.delete_column(u'bcpp_household_householdstructure_audit', '_audit_subject_identifier')

        # Deleting field 'HouseholdStructureAudit.enrolled'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'enrolled')

        # Deleting field 'HouseholdStructureAudit.enrolled_household_member'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'enrolled_household_member')

        # Deleting field 'HouseholdStructureAudit.enrolled_datetime'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'enrolled_datetime')

        # Deleting field 'HouseholdStructureAudit.enumerated'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'enumerated')

        # Deleting field 'HouseholdStructureAudit.enumeration_attempts'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'enumeration_attempts')

        # Deleting field 'HouseholdStructureAudit.refused_enumeration'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'refused_enumeration')

        # Deleting field 'HouseholdStructureAudit.failed_enumeration_attempts'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'failed_enumeration_attempts')

        # Deleting field 'HouseholdStructureAudit.failed_enumeration'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'failed_enumeration')

        # Deleting field 'HouseholdStructureAudit.no_informant'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'no_informant')

        # Deleting field 'HouseholdStructureAudit.eligible_members'
        db.delete_column(u'bcpp_household_householdstructure_audit', 'eligible_members')


        # Changing field 'HouseholdStructureAudit.revision'
        db.alter_column(u'bcpp_household_householdstructure_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Deleting field 'HouseholdAudit._audit_subject_identifier'
        db.delete_column(u'bcpp_household_household_audit', '_audit_subject_identifier')

        # Deleting field 'HouseholdAudit.replaced_by'
        db.delete_column(u'bcpp_household_household_audit', 'replaced_by')

        # Deleting field 'HouseholdAudit.enrolled'
        db.delete_column(u'bcpp_household_household_audit', 'enrolled')

        # Deleting field 'HouseholdAudit.complete'
        db.delete_column(u'bcpp_household_household_audit', 'complete')


        # Changing field 'HouseholdAudit.revision'
        db.alter_column(u'bcpp_household_household_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'HouseholdIdentifierHistory.revision'
        db.alter_column(u'bcpp_household_householdidentifierhistory', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Deleting field 'HouseholdLogAudit._audit_subject_identifier'
        db.delete_column(u'bcpp_household_householdlog_audit', '_audit_subject_identifier')


        # Changing field 'HouseholdLogAudit.revision'
        db.alter_column(u'bcpp_household_householdlog_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Deleting field 'Household.replaced_by'
        db.delete_column(u'bcpp_household_household', 'replaced_by')

        # Deleting field 'Household.enrolled'
        db.delete_column(u'bcpp_household_household', 'enrolled')

        # Deleting field 'Household.complete'
        db.delete_column(u'bcpp_household_household', 'complete')


        # Changing field 'Household.revision'
        db.alter_column(u'bcpp_household_household', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))
        # Deleting field 'PlotAudit._audit_subject_identifier'
        db.delete_column(u'bcpp_household_plot_audit', '_audit_subject_identifier')

        # Deleting field 'PlotAudit.comment'
        db.delete_column(u'bcpp_household_plot_audit', 'comment')

        # Deleting field 'PlotAudit.distance_from_target'
        db.delete_column(u'bcpp_household_plot_audit', 'distance_from_target')

        # Deleting field 'PlotAudit.replaces'
        db.delete_column(u'bcpp_household_plot_audit', 'replaces')

        # Deleting field 'PlotAudit.access_attempts'
        db.delete_column(u'bcpp_household_plot_audit', 'access_attempts')

        # Deleting field 'PlotAudit.bhs'
        db.delete_column(u'bcpp_household_plot_audit', 'bhs')

        # Deleting field 'PlotAudit.replaced_by'
        db.delete_column(u'bcpp_household_plot_audit', 'replaced_by')


        # Changing field 'PlotAudit.revision'
        db.alter_column(u'bcpp_household_plot_audit', 'revision', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'PlotAudit.status'
        db.alter_column(u'bcpp_household_plot_audit', 'status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'PlotAudit.uploaded_map_18'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_18', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'PlotAudit.uploaded_map_17'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_17', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'PlotAudit.uploaded_map_16'
        db.alter_column(u'bcpp_household_plot_audit', 'uploaded_map_16', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    models = {
        'bcpp_household.community': {
            'Meta': {'object_name': 'Community'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enrolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_household'", 'null': 'True', 'to': "orm['bcpp_household.Plot']"}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'Meta': {'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'eligible_members': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enrolled': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'enrolled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'enrolled_household_member': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'enumerated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'failed_enumeration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'failed_enumeration_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
        'bcpp_household.plot': {
            'Meta': {'ordering': "['-plot_identifier']", 'unique_together': "(('gps_target_lat', 'gps_target_lon'),)", 'object_name': 'Plot'},
            'access_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'bhs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'distance_from_target': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
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
            'bhs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'distance_from_target': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'log_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.PlotLog']"}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'log_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_plotlogentry'", 'to': "orm['bcpp_household.PlotLog']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.replacementhistory': {
            'Meta': {'ordering': "['-replacing_item']", 'unique_together': "(('replacing_item', 'replaced_item'),)", 'object_name': 'ReplacementHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'replaced_item': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'replacement_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'replacement_reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'replacing_item': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'replaced_item': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'replacement_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'replacement_reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'replacing_item': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.representativeeligibility': {
            'Meta': {'object_name': 'RepresentativeEligibility'},
            'aged_over_18': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubjectOffStudyAudit'
        db.create_table('bcpp_subject_subjectoffstudy_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('offstudy_date', self.gf('django.db.models.fields.DateField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('has_scheduled_data', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectoffstudy', to=orm['bhp_registration.RegisteredSubject'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectOffStudyAudit'])

        # Adding model 'SubjectOffStudy'
        db.create_table('bcpp_subject_subjectoffstudy', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True)),
            ('offstudy_date', self.gf('django.db.models.fields.DateField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('has_scheduled_data', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectOffStudy'])

        # Adding model 'SubjectConsentAudit'
        db.create_table('bcpp_subject_subjectconsent_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectconsent', to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectconsent', to=orm['bhp_registration.RegisteredSubject'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectconsent', to=orm['bcpp_survey.Survey'])),
            ('is_signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_minor', self.gf('django.db.models.fields.CharField')(default='-', max_length=10, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('household_member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectconsent', to=orm['bcpp_household_member.HouseholdMember'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectConsentAudit'])

        # Adding model 'SubjectConsent'
        db.create_table('bcpp_subject_subjectconsent', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=78L)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'])),
            ('household_member', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household_member.HouseholdMember'], unique=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('is_signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_minor', self.gf('django.db.models.fields.CharField')(default='-', max_length=10, null=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectConsent'])

        # Adding model 'SubjectVisitAudit'
        db.create_table('bcpp_subject_subjectvisit_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reason_unscheduled', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('appointment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectvisit', to=orm['bhp_appointment.Appointment'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectVisitAudit'])

        # Adding model 'SubjectVisit'
        db.create_table('bcpp_subject_subjectvisit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_appointment.Appointment'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reason_unscheduled', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectVisit'])

        # Adding model 'SubjectLocatorAudit'
        db.create_table('bcpp_subject_subjectlocator_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_signed', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('mail_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('home_visit_permission', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('may_follow_up', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_cell_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_call_work', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_work_place', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('subject_work_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_contact_someone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_rel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectlocator', null=True, to=orm['bcpp_subject.SubjectVisit'])),
            ('alt_contact_cell_number', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('has_alt_contact', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alt_contact_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_rel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('other_alt_contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_tel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectlocator', null=True, to=orm['bhp_registration.RegisteredSubject'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectLocatorAudit'])

        # Adding model 'SubjectLocator'
        db.create_table('bcpp_subject_subjectlocator', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True, null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_signed', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('mail_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('home_visit_permission', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('may_follow_up', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_cell_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_call_work', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_work_place', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('subject_work_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_contact_someone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_rel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_subject.SubjectVisit'], null=True)),
            ('alt_contact_cell_number', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('has_alt_contact', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alt_contact_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_rel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('other_alt_contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('alt_contact_tel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectLocator'])

        # Adding model 'SubjectDeathAudit'
        db.create_table('bcpp_subject_subjectdeath_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('death_date', self.gf('django.db.models.fields.DateField')()),
            ('death_cause_info', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectdeath', to=orm['bhp_adverse.DeathCauseInfo'])),
            ('death_cause_info_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('death_cause', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('death_cause_category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectdeath', to=orm['bhp_adverse.DeathCauseCategory'])),
            ('death_cause_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('participant_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('death_reason_hospitalized', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_audit_subjectdeath', null=True, to=orm['bhp_adverse.DeathReasonHospitalized'])),
            ('days_hospitalized', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('sufficient_records', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_hiv', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_community', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_community_other', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('death_year', self.gf('django.db.models.fields.DateField')()),
            ('decendent_death_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('hospital_death', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('decedent_haart', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('decedent_haart_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('decedent_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('days_decedent_hospitalized', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hospital_visits', self.gf('django.db.models.fields.IntegerField')()),
            ('doctor_evaluation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectdeath', to=orm['bhp_registration.RegisteredSubject'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectDeathAudit'])

        # Adding model 'SubjectDeath'
        db.create_table('bcpp_subject_subjectdeath', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True)),
            ('death_date', self.gf('django.db.models.fields.DateField')()),
            ('death_cause_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_adverse.DeathCauseInfo'])),
            ('death_cause_info_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('death_cause', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('death_cause_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_adverse.DeathCauseCategory'])),
            ('death_cause_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('participant_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('death_reason_hospitalized', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_adverse.DeathReasonHospitalized'], null=True, blank=True)),
            ('days_hospitalized', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('sufficient_records', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_hiv', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_community', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('document_community_other', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('death_year', self.gf('django.db.models.fields.DateField')()),
            ('decendent_death_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('hospital_death', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('decedent_haart', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('decedent_haart_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('decedent_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('days_decedent_hospitalized', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hospital_visits', self.gf('django.db.models.fields.IntegerField')()),
            ('doctor_evaluation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectDeath'])

        # Adding model 'RecentPartnerAudit'
        db.create_table('bcpp_subject_recentpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_recentpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['RecentPartnerAudit'])

        # Adding model 'RecentPartner'
        db.create_table('bcpp_subject_recentpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['RecentPartner'])

        # Adding model 'SecondPartnerAudit'
        db.create_table('bcpp_subject_secondpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_secondpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['SecondPartnerAudit'])

        # Adding model 'SecondPartner'
        db.create_table('bcpp_subject_secondpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SecondPartner'])

        # Adding model 'ThirdPartnerAudit'
        db.create_table('bcpp_subject_thirdpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_thirdpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['ThirdPartnerAudit'])

        # Adding model 'ThirdPartner'
        db.create_table('bcpp_subject_thirdpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('rel_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('partner_gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('last_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('last_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_sex_contact', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_contact_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('regular_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('having_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('having_sex_reg', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alcohol_before_sex', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('partner_status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('partner_arv', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('status_disclosure', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('multiple_partners', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('intercourse_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['ThirdPartner'])

        # Adding model 'QualityOfLifeAudit'
        db.create_table('bcpp_subject_qualityoflife_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('mobility', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('self_care', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('activities', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pain', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('anxiety', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('health_today', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_qualityoflife', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['QualityOfLifeAudit'])

        # Adding model 'QualityOfLife'
        db.create_table('bcpp_subject_qualityoflife', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('mobility', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('self_care', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('activities', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pain', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('anxiety', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('health_today', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['QualityOfLife'])

        # Adding model 'ResourceUtilizationAudit'
        db.create_table('bcpp_subject_resourceutilization_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('out_patient', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('hospitalized', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('money_spent', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('medical_cover', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_resourceutilization', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['ResourceUtilizationAudit'])

        # Adding model 'ResourceUtilization'
        db.create_table('bcpp_subject_resourceutilization', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('out_patient', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('hospitalized', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('money_spent', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('medical_cover', self.gf('django.db.models.fields.CharField')(max_length=17)),
        ))
        db.send_create_signal('bcpp_subject', ['ResourceUtilization'])

        # Adding model 'OutpatientCareAudit'
        db.create_table('bcpp_subject_outpatientcare_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('govt_health_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('dept_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('prvt_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('trad_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('care_visits', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('facility_visited', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('specific_clinic', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('care_reason', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('care_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('outpatient_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('travel_time', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('transport_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('cost_cover', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('waiting_hours', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_outpatientcare', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['OutpatientCareAudit'])

        # Adding model 'OutpatientCare'
        db.create_table('bcpp_subject_outpatientcare', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('govt_health_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('dept_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('prvt_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('trad_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('care_visits', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('facility_visited', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('specific_clinic', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('care_reason', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('care_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('outpatient_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('travel_time', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('transport_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('cost_cover', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('waiting_hours', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['OutpatientCare'])

        # Adding model 'HospitalAdmissionAudit'
        db.create_table('bcpp_subject_hospitaladmission_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('admission_nights', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('reason_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('facility_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('nights_hospitalized', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('healthcare_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('travel_hours', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total_expenses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hospitalization_costs', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hospitaladmission', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HospitalAdmissionAudit'])

        # Adding model 'HospitalAdmission'
        db.create_table('bcpp_subject_hospitaladmission', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('admission_nights', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('reason_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('facility_hospitalized', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('nights_hospitalized', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('healthcare_expense', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('travel_hours', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('total_expenses', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('hospitalization_costs', self.gf('django.db.models.fields.CharField')(max_length=17)),
        ))
        db.send_create_signal('bcpp_subject', ['HospitalAdmission'])

        # Adding model 'HivHealthCareCostsAudit'
        db.create_table('bcpp_subject_hivhealthcarecosts_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_medical_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('reason_no_care', self.gf('django.db.models.fields.CharField')(max_length=115, null=True, blank=True)),
            ('place_care_received', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('care_regularity', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('doctor_visits', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivhealthcarecosts', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivHealthCareCostsAudit'])

        # Adding model 'HivHealthCareCosts'
        db.create_table('bcpp_subject_hivhealthcarecosts', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_medical_care', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('reason_no_care', self.gf('django.db.models.fields.CharField')(max_length=115, null=True, blank=True)),
            ('place_care_received', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('care_regularity', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('doctor_visits', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('bcpp_subject', ['HivHealthCareCosts'])

        # Adding model 'LabourMarketWagesAudit'
        db.create_table('bcpp_subject_labourmarketwages_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('employed', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('occupation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('job_description_change', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('days_worked', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('monthly_income', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('salary_payment', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('household_income', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('other_occupation', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('other_occupation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('govt_grant', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('weeks_out', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('days_not_worked', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('days_inactivite', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_labourmarketwages', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['LabourMarketWagesAudit'])

        # Adding model 'LabourMarketWages'
        db.create_table('bcpp_subject_labourmarketwages', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('employed', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('occupation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('job_description_change', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('days_worked', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('monthly_income', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('salary_payment', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('household_income', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('other_occupation', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('other_occupation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('govt_grant', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('nights_out', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('weeks_out', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('days_not_worked', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('days_inactivite', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['LabourMarketWages'])

        # Adding model 'GrantAudit'
        db.create_table('bcpp_subject_grant_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('grant_number', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('grant_type', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('other_grant', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('labour_market_wages', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_grant', to=orm['bcpp_subject.LabourMarketWages'])),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_subject', ['GrantAudit'])

        # Adding model 'Grant'
        db.create_table('bcpp_subject_grant', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('grant_number', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('grant_type', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('other_grant', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('labour_market_wages', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_subject.LabourMarketWages'])),
        ))
        db.send_create_signal('bcpp_subject', ['Grant'])

        # Adding model 'BaselineHouseholdSurveyAudit'
        db.create_table('bcpp_subject_baselinehouseholdsurvey_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('flooring_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('flooring_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('living_rooms', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('water_source', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('water_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('energy_source', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('energy_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('toilet_facility', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('toilet_facility_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('goats_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('sheep_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('cattle_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('smaller_meals', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_baselinehouseholdsurvey', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['BaselineHouseholdSurveyAudit'])

        # Adding model 'BaselineHouseholdSurvey'
        db.create_table('bcpp_subject_baselinehouseholdsurvey', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('flooring_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('flooring_type_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('living_rooms', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('water_source', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('water_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('energy_source', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('energy_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('toilet_facility', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('toilet_facility_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('goats_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('sheep_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('cattle_owned', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('smaller_meals', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['BaselineHouseholdSurvey'])

        # Adding M2M table for field electrical_appliances on 'BaselineHouseholdSurvey'
        db.create_table('bcpp_subject_baselinehouseholdsurvey_electrical_appliances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('baselinehouseholdsurvey', models.ForeignKey(orm['bcpp_subject.baselinehouseholdsurvey'], null=False)),
            ('electricalappliances', models.ForeignKey(orm['bcpp_list.electricalappliances'], null=False))
        ))
        db.create_unique('bcpp_subject_baselinehouseholdsurvey_electrical_appliances', ['baselinehouseholdsurvey_id', 'electricalappliances_id'])

        # Adding M2M table for field transport_mode on 'BaselineHouseholdSurvey'
        db.create_table('bcpp_subject_baselinehouseholdsurvey_transport_mode', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('baselinehouseholdsurvey', models.ForeignKey(orm['bcpp_subject.baselinehouseholdsurvey'], null=False)),
            ('transportmode', models.ForeignKey(orm['bcpp_list.transportmode'], null=False))
        ))
        db.create_unique('bcpp_subject_baselinehouseholdsurvey_transport_mode', ['baselinehouseholdsurvey_id', 'transportmode_id'])

        # Adding model 'CeaEnrolmentChecklistAudit'
        db.create_table('bcpp_subject_ceaenrolmentchecklist_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('mental_capacity', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('incarceration', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('citizen', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('community_resident', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('enrolment_reason', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('cd4_date', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('cd4_count', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('opportunistic_illness', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('diagnosis_date', self.gf('django.db.models.fields.DateField')(max_length=3)),
            ('date_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_ceaenrolmentchecklist', to=orm['bhp_registration.RegisteredSubject'])),
        ))
        db.send_create_signal('bcpp_subject', ['CeaEnrolmentChecklistAudit'])

        # Adding model 'CeaEnrolmentChecklist'
        db.create_table('bcpp_subject_ceaenrolmentchecklist', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True)),
            ('mental_capacity', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('incarceration', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('citizen', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('community_resident', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('enrolment_reason', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('cd4_date', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('cd4_count', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('opportunistic_illness', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('diagnosis_date', self.gf('django.db.models.fields.DateField')(max_length=3)),
            ('date_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['CeaEnrolmentChecklist'])

        # Adding model 'CsEnrolmentChecklistAudit'
        db.create_table('bcpp_subject_csenrolmentchecklist_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('registration_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('census_number', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('mental_capacity', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('incarceration', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('citizen', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('community_resident', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('date_minor_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25, null=True, blank=True)),
            ('date_guardian_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25, null=True, blank=True)),
            ('date_consent_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_csenrolmentchecklist', to=orm['bhp_registration.RegisteredSubject'])),
        ))
        db.send_create_signal('bcpp_subject', ['CsEnrolmentChecklistAudit'])

        # Adding model 'CsEnrolmentChecklist'
        db.create_table('bcpp_subject_csenrolmentchecklist', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True)),
            ('registration_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('census_number', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('mental_capacity', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('incarceration', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('citizen', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('community_resident', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('date_minor_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25, null=True, blank=True)),
            ('date_guardian_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25, null=True, blank=True)),
            ('date_consent_signed', self.gf('django.db.models.fields.DateTimeField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['CsEnrolmentChecklist'])

        # Adding model 'ResidencyMobilityAudit'
        db.create_table('bcpp_subject_residencymobility_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('length_residence', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('forteen_nights', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('intend_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('nights_away', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('cattle_postlands', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=25)),
            ('cattle_postlands_other', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_residencymobility', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['ResidencyMobilityAudit'])

        # Adding model 'ResidencyMobility'
        db.create_table('bcpp_subject_residencymobility', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('length_residence', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('forteen_nights', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('intend_residency', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('nights_away', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('cattle_postlands', self.gf('django.db.models.fields.CharField')(default='N/A', max_length=25)),
            ('cattle_postlands_other', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['ResidencyMobility'])

        # Adding model 'DemographicsAudit'
        db.create_table('bcpp_subject_demographics_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('religion_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('ethnic', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('marital_status', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('num_wives', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('husband_wives', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_demographics', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['DemographicsAudit'])

        # Adding model 'Demographics'
        db.create_table('bcpp_subject_demographics', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('religion_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('ethnic', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('marital_status', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('num_wives', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('husband_wives', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['Demographics'])

        # Adding M2M table for field religion on 'Demographics'
        db.create_table('bcpp_subject_demographics_religion', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('demographics', models.ForeignKey(orm['bcpp_subject.demographics'], null=False)),
            ('religion', models.ForeignKey(orm['bcpp_list.religion'], null=False))
        ))
        db.create_unique('bcpp_subject_demographics_religion', ['demographics_id', 'religion_id'])

        # Adding M2M table for field live_with on 'Demographics'
        db.create_table('bcpp_subject_demographics_live_with', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('demographics', models.ForeignKey(orm['bcpp_subject.demographics'], null=False)),
            ('livewith', models.ForeignKey(orm['bcpp_list.livewith'], null=False))
        ))
        db.create_unique('bcpp_subject_demographics_live_with', ['demographics_id', 'livewith_id'])

        # Adding model 'CommunityEngagementAudit'
        db.create_table('bcpp_subject_communityengagement_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('community_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('vote_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('problems_engagement_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('solve_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_communityengagement', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['CommunityEngagementAudit'])

        # Adding model 'CommunityEngagement'
        db.create_table('bcpp_subject_communityengagement', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('community_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('vote_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('problems_engagement_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('solve_engagement', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['CommunityEngagement'])

        # Adding M2M table for field problems_engagement on 'CommunityEngagement'
        db.create_table('bcpp_subject_communityengagement_problems_engagement', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('communityengagement', models.ForeignKey(orm['bcpp_subject.communityengagement'], null=False)),
            ('neighbourhoodproblems', models.ForeignKey(orm['bcpp_list.neighbourhoodproblems'], null=False))
        ))
        db.create_unique('bcpp_subject_communityengagement_problems_engagement', ['communityengagement_id', 'neighbourhoodproblems_id'])

        # Adding model 'EducationAudit'
        db.create_table('bcpp_subject_education_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('working', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('reason_unemployed', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('job_description', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('monthly_income', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_education', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['EducationAudit'])

        # Adding model 'Education'
        db.create_table('bcpp_subject_education', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('working', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('reason_unemployed', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('job_description', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('monthly_income', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['Education'])

        # Adding model 'HivTestingHistoryAudit'
        db.create_table('bcpp_subject_hivtestinghistory_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('has_tested', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('when_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('has_record', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('verbal_hiv_result', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('other_record', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivtestinghistory', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivTestingHistoryAudit'])

        # Adding model 'HivTestingHistory'
        db.create_table('bcpp_subject_hivtestinghistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('has_tested', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('when_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('has_record', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('verbal_hiv_result', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('other_record', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_subject', ['HivTestingHistory'])

        # Adding model 'HivTestReviewAudit'
        db.create_table('bcpp_subject_hivtestreview_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_test_date', self.gf('django.db.models.fields.DateField')()),
            ('recorded_hiv_result', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivtestreview', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivTestReviewAudit'])

        # Adding model 'HivTestReview'
        db.create_table('bcpp_subject_hivtestreview', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_test_date', self.gf('django.db.models.fields.DateField')()),
            ('recorded_hiv_result', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('bcpp_subject', ['HivTestReview'])

        # Adding model 'HivTestedAudit'
        db.create_table('bcpp_subject_hivtested_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_pills', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arvs_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('num_hiv_tests', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('where_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=85, null=True, blank=True)),
            ('why_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=105, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivtested', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivTestedAudit'])

        # Adding model 'HivTested'
        db.create_table('bcpp_subject_hivtested', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_pills', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arvs_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('num_hiv_tests', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('where_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=85, null=True, blank=True)),
            ('why_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=105, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['HivTested'])

        # Adding model 'HivUntestedAudit'
        db.create_table('bcpp_subject_hivuntested_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_pills', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arvs_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('why_no_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivuntested', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivUntestedAudit'])

        # Adding model 'HivUntested'
        db.create_table('bcpp_subject_hivuntested', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_pills', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arvs_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('why_no_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['HivUntested'])

        # Adding model 'FutureHivTestingAudit'
        db.create_table('bcpp_subject_futurehivtesting_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('prefer_hivtest', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('hiv_test_time', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('hiv_test_time_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('hiv_test_week', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('hiv_test_week_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('hiv_test_year', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hiv_test_year_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_futurehivtesting', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['FutureHivTestingAudit'])

        # Adding model 'FutureHivTesting'
        db.create_table('bcpp_subject_futurehivtesting', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('prefer_hivtest', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('hiv_test_time', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('hiv_test_time_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('hiv_test_week', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('hiv_test_week_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('hiv_test_year', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hiv_test_year_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['FutureHivTesting'])

        # Adding model 'SexualBehaviourAudit'
        db.create_table('bcpp_subject_sexualbehaviour_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('ever_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_year_partners', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('more_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('condom', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('alcohol_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_sexualbehaviour', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['SexualBehaviourAudit'])

        # Adding model 'SexualBehaviour'
        db.create_table('bcpp_subject_sexualbehaviour', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('ever_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_year_partners', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('more_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_sex', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('condom', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('alcohol_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_sex', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SexualBehaviour'])

        # Adding model 'MonthsRecentPartnerAudit'
        db.create_table('bcpp_subject_monthsrecentpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_monthsrecentpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsRecentPartnerAudit'])

        # Adding model 'MonthsRecentPartner'
        db.create_table('bcpp_subject_monthsrecentpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsRecentPartner'])

        # Adding M2M table for field first_partner_live on 'MonthsRecentPartner'
        db.create_table('bcpp_subject_monthsrecentpartner_first_partner_live', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthsrecentpartner', models.ForeignKey(orm['bcpp_subject.monthsrecentpartner'], null=False)),
            ('partnerresidency', models.ForeignKey(orm['bcpp_list.partnerresidency'], null=False))
        ))
        db.create_unique('bcpp_subject_monthsrecentpartner_first_partner_live', ['monthsrecentpartner_id', 'partnerresidency_id'])

        # Adding model 'MonthsSecondPartnerAudit'
        db.create_table('bcpp_subject_monthssecondpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_monthssecondpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsSecondPartnerAudit'])

        # Adding model 'MonthsSecondPartner'
        db.create_table('bcpp_subject_monthssecondpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsSecondPartner'])

        # Adding M2M table for field first_partner_live on 'MonthsSecondPartner'
        db.create_table('bcpp_subject_monthssecondpartner_first_partner_live', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthssecondpartner', models.ForeignKey(orm['bcpp_subject.monthssecondpartner'], null=False)),
            ('partnerresidency', models.ForeignKey(orm['bcpp_list.partnerresidency'], null=False))
        ))
        db.create_unique('bcpp_subject_monthssecondpartner_first_partner_live', ['monthssecondpartner_id', 'partnerresidency_id'])

        # Adding model 'MonthsThirdPartnerAudit'
        db.create_table('bcpp_subject_monthsthirdpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_monthsthirdpartner', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsThirdPartnerAudit'])

        # Adding model 'MonthsThirdPartner'
        db.create_table('bcpp_subject_monthsthirdpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('third_last_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('third_last_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_first_sex', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_first_sex_calc', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_sex_current', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_relationship', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('first_exchange', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('concurrent', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('goods_exchange', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_sex_freq', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('first_partner_hiv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_haart', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('first_disclose', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_condom_freq', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('first_partner_cp', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
        ))
        db.send_create_signal('bcpp_subject', ['MonthsThirdPartner'])

        # Adding M2M table for field first_partner_live on 'MonthsThirdPartner'
        db.create_table('bcpp_subject_monthsthirdpartner_first_partner_live', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('monthsthirdpartner', models.ForeignKey(orm['bcpp_subject.monthsthirdpartner'], null=False)),
            ('partnerresidency', models.ForeignKey(orm['bcpp_list.partnerresidency'], null=False))
        ))
        db.create_unique('bcpp_subject_monthsthirdpartner_first_partner_live', ['monthsthirdpartner_id', 'partnerresidency_id'])

        # Adding model 'HivCareAdherenceAudit'
        db.create_table('bcpp_subject_hivcareadherence_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('first_positive', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('medical_care', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('no_medical_care', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('ever_recommended_arv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('arv_naive', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('why_no_arv', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('why_no_arv_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_arv', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('on_arv', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arv_stop_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('arv_stop', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('arv_stop_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('adherence_4_day', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('adherence_4_wk', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivcareadherence', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivCareAdherenceAudit'])

        # Adding model 'HivCareAdherence'
        db.create_table('bcpp_subject_hivcareadherence', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('first_positive', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('medical_care', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('no_medical_care', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('ever_recommended_arv', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('arv_naive', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('why_no_arv', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('why_no_arv_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('first_arv', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('on_arv', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('arv_stop_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('arv_stop', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('arv_stop_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('adherence_4_day', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('adherence_4_wk', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['HivCareAdherence'])

        # Adding model 'HivMedicalCareAudit'
        db.create_table('bcpp_subject_hivmedicalcare_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('first_hiv_care_pos', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('last_hiv_care_pos', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('lowest_cd4', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivmedicalcare', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivMedicalCareAudit'])

        # Adding model 'HivMedicalCare'
        db.create_table('bcpp_subject_hivmedicalcare', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('first_hiv_care_pos', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('last_hiv_care_pos', self.gf('django.db.models.fields.DateField')(max_length=25)),
            ('lowest_cd4', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['HivMedicalCare'])

        # Adding model 'CircumcisionAudit'
        db.create_table('bcpp_subject_circumcision_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_circumcision', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['CircumcisionAudit'])

        # Adding model 'Circumcision'
        db.create_table('bcpp_subject_circumcision', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('bcpp_subject', ['Circumcision'])

        # Adding model 'CircumcisedAudit'
        db.create_table('bcpp_subject_circumcised_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('when_circ', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('where_circ', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('where_circ_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('why_circ', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('why_circ_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_circumcised', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['CircumcisedAudit'])

        # Adding model 'Circumcised'
        db.create_table('bcpp_subject_circumcised', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('when_circ', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('where_circ', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('where_circ_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('why_circ', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('why_circ_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['Circumcised'])

        # Adding M2M table for field health_benefits_smc on 'Circumcised'
        db.create_table('bcpp_subject_circumcised_health_benefits_smc', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circumcised', models.ForeignKey(orm['bcpp_subject.circumcised'], null=False)),
            ('circumcisionbenefits', models.ForeignKey(orm['bcpp_list.circumcisionbenefits'], null=False))
        ))
        db.create_unique('bcpp_subject_circumcised_health_benefits_smc', ['circumcised_id', 'circumcisionbenefits_id'])

        # Adding model 'UncircumcisedAudit'
        db.create_table('bcpp_subject_uncircumcised_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reason_circ', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('future_circ', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_day_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('circumcision_week', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_week_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('circumcision_year', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_year_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('future_reasons_smc', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('service_facilities', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('aware_free', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_uncircumcised', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['UncircumcisedAudit'])

        # Adding model 'Uncircumcised'
        db.create_table('bcpp_subject_uncircumcised', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('circumcised', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reason_circ', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('future_circ', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_day', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_day_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('circumcision_week', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_week_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('circumcision_year', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_year_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('future_reasons_smc', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('service_facilities', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('aware_free', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['Uncircumcised'])

        # Adding M2M table for field health_benefits_smc on 'Uncircumcised'
        db.create_table('bcpp_subject_uncircumcised_health_benefits_smc', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('uncircumcised', models.ForeignKey(orm['bcpp_subject.uncircumcised'], null=False)),
            ('circumcisionbenefits', models.ForeignKey(orm['bcpp_list.circumcisionbenefits'], null=False))
        ))
        db.create_unique('bcpp_subject_uncircumcised_health_benefits_smc', ['uncircumcised_id', 'circumcisionbenefits_id'])

        # Adding model 'ReproductiveHealthAudit'
        db.create_table('bcpp_subject_reproductivehealth_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('number_children', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('menopause', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_reproductivehealth', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['ReproductiveHealthAudit'])

        # Adding model 'ReproductiveHealth'
        db.create_table('bcpp_subject_reproductivehealth', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('number_children', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('menopause', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_subject', ['ReproductiveHealth'])

        # Adding model 'MedicalDiagnosesAudit'
        db.create_table('bcpp_subject_medicaldiagnoses_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('heart_attack_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('cancer_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sti', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('tb_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_medicaldiagnoses', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['MedicalDiagnosesAudit'])

        # Adding model 'MedicalDiagnoses'
        db.create_table('bcpp_subject_medicaldiagnoses', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('heart_attack_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('cancer_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sti', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('tb_record', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['MedicalDiagnoses'])

        # Adding M2M table for field diagnoses on 'MedicalDiagnoses'
        db.create_table('bcpp_subject_medicaldiagnoses_diagnoses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medicaldiagnoses', models.ForeignKey(orm['bcpp_subject.medicaldiagnoses'], null=False)),
            ('diagnoses', models.ForeignKey(orm['bcpp_list.diagnoses'], null=False))
        ))
        db.create_unique('bcpp_subject_medicaldiagnoses_diagnoses', ['medicaldiagnoses_id', 'diagnoses_id'])

        # Adding model 'HeartAttackAudit'
        db.create_table('bcpp_subject_heartattack_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_heart_attack', self.gf('django.db.models.fields.DateField')()),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_heartattack', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HeartAttackAudit'])

        # Adding model 'HeartAttack'
        db.create_table('bcpp_subject_heartattack', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_heart_attack', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('bcpp_subject', ['HeartAttack'])

        # Adding M2M table for field dx_heart_attack on 'HeartAttack'
        db.create_table('bcpp_subject_heartattack_dx_heart_attack', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('heartattack', models.ForeignKey(orm['bcpp_subject.heartattack'], null=False)),
            ('heartdisease', models.ForeignKey(orm['bcpp_list.heartdisease'], null=False))
        ))
        db.create_unique('bcpp_subject_heartattack_dx_heart_attack', ['heartattack_id', 'heartdisease_id'])

        # Adding model 'CancerAudit'
        db.create_table('bcpp_subject_cancer_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_cancer', self.gf('django.db.models.fields.DateField')()),
            ('dx_cancer', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_cancer', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['CancerAudit'])

        # Adding model 'Cancer'
        db.create_table('bcpp_subject_cancer', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_cancer', self.gf('django.db.models.fields.DateField')()),
            ('dx_cancer', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('bcpp_subject', ['Cancer'])

        # Adding model 'TubercolosisAudit'
        db.create_table('bcpp_subject_tubercolosis_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_tb', self.gf('django.db.models.fields.DateField')()),
            ('dx_tb', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_tubercolosis', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['TubercolosisAudit'])

        # Adding model 'Tubercolosis'
        db.create_table('bcpp_subject_tubercolosis', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('date_tb', self.gf('django.db.models.fields.DateField')()),
            ('dx_tb', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('bcpp_subject', ['Tubercolosis'])

        # Adding model 'SubstanceUseAudit'
        db.create_table('bcpp_subject_substanceuse_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('alcohol', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('smoke', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_substanceuse', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubstanceUseAudit'])

        # Adding model 'SubstanceUse'
        db.create_table('bcpp_subject_substanceuse', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('alcohol', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('smoke', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['SubstanceUse'])

        # Adding model 'StigmaAudit'
        db.create_table('bcpp_subject_stigma_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('anticipate_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_shame_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('saliva_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('teacher_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('children_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_stigma', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['StigmaAudit'])

        # Adding model 'Stigma'
        db.create_table('bcpp_subject_stigma', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('anticipate_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_shame_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('saliva_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('teacher_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('children_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['Stigma'])

        # Adding model 'StigmaOpinionAudit'
        db.create_table('bcpp_subject_stigmaopinion_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('test_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gossip_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('respect_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_verbal_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_phyical_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_family_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('fear_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_stigmaopinion', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['StigmaOpinionAudit'])

        # Adding model 'StigmaOpinion'
        db.create_table('bcpp_subject_stigmaopinion', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('test_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('gossip_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('respect_community_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_verbal_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_phyical_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_family_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('fear_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['StigmaOpinion'])

        # Adding model 'PositiveParticipantAudit'
        db.create_table('bcpp_subject_positiveparticipant_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('internalize_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('internalized_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('friend_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('family_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_talk_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_respect_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_jobs_tigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_positiveparticipant', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['PositiveParticipantAudit'])

        # Adding model 'PositiveParticipant'
        db.create_table('bcpp_subject_positiveparticipant', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('internalize_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('internalized_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('friend_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('family_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_talk_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_respect_stigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('enacted_jobs_tigma', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['PositiveParticipant'])

        # Adding model 'AccessToCareAudit'
        db.create_table('bcpp_subject_accesstocare_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('access_care', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('access_care_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('medical_care_access_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('overall_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('emergency_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('expensive_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('convenient_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('whenever_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_accesstocare', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['AccessToCareAudit'])

        # Adding model 'AccessToCare'
        db.create_table('bcpp_subject_accesstocare', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('access_care', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('access_care_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('medical_care_access_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('overall_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('emergency_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('expensive_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('convenient_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('whenever_access', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['AccessToCare'])

        # Adding M2M table for field medical_care_access on 'AccessToCare'
        db.create_table('bcpp_subject_accesstocare_medical_care_access', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accesstocare', models.ForeignKey(orm['bcpp_subject.accesstocare'], null=False)),
            ('medicalcareaccess', models.ForeignKey(orm['bcpp_list.medicalcareaccess'], null=False))
        ))
        db.create_unique('bcpp_subject_accesstocare_medical_care_access', ['accesstocare_id', 'medicalcareaccess_id'])

        # Adding model 'TodaysHivResultAudit'
        db.create_table('bcpp_subject_todayshivresult_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_result', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('why_not_tested', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_todayshivresult', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['TodaysHivResultAudit'])

        # Adding model 'TodaysHivResult'
        db.create_table('bcpp_subject_todayshivresult', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('hiv_result', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('why_not_tested', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['TodaysHivResult'])

        # Adding model 'PregnancyAudit'
        db.create_table('bcpp_subject_pregnancy_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('more_children', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('where_circ', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('family_planning_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('current_pregnant', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('anc_reg', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
            ('lnmp', self.gf('django.db.models.fields.DateField')()),
            ('last_birth', self.gf('django.db.models.fields.DateField')()),
            ('anc_last_pregnancy', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hiv_last_pregnancy', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('preg_arv', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_pregnancy', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['PregnancyAudit'])

        # Adding model 'Pregnancy'
        db.create_table('bcpp_subject_pregnancy', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('more_children', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('where_circ', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('family_planning_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('current_pregnant', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('anc_reg', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
            ('lnmp', self.gf('django.db.models.fields.DateField')()),
            ('last_birth', self.gf('django.db.models.fields.DateField')()),
            ('anc_last_pregnancy', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hiv_last_pregnancy', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('preg_arv', self.gf('django.db.models.fields.CharField')(max_length=95)),
        ))
        db.send_create_signal('bcpp_subject', ['Pregnancy'])

        # Adding M2M table for field family_planning on 'Pregnancy'
        db.create_table('bcpp_subject_pregnancy_family_planning', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pregnancy', models.ForeignKey(orm['bcpp_subject.pregnancy'], null=False)),
            ('familyplanning', models.ForeignKey(orm['bcpp_list.familyplanning'], null=False))
        ))
        db.create_unique('bcpp_subject_pregnancy_family_planning', ['pregnancy_id', 'familyplanning_id'])

        # Adding model 'HivResultDocumentationAudit'
        db.create_table('bcpp_subject_hivresultdocumentation_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('result_date', self.gf('django.db.models.fields.DateField')()),
            ('result_recorded', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('result_doc_type', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivresultdocumentation', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HivResultDocumentationAudit'])

        # Adding model 'HivResultDocumentation'
        db.create_table('bcpp_subject_hivresultdocumentation', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('result_date', self.gf('django.db.models.fields.DateField')()),
            ('result_recorded', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('result_doc_type', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('bcpp_subject', ['HivResultDocumentation'])

        # Adding model 'SubjectRefusalAudit'
        db.create_table('bcpp_subject_subjectrefusal_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectrefusal', null=True, to=orm['bhp_registration.RegisteredSubject'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectrefusal', to=orm['bcpp_survey.Survey'])),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('length_residence', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('refusal_date', self.gf('django.db.models.fields.DateField')()),
            ('why_no_participate', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('why_no_participate_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('subject_refusal_status', self.gf('django.db.models.fields.CharField')(default='REFUSED', max_length=25)),
            ('hiv_test_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('why_no_hivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('household_member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectrefusal', to=orm['bcpp_household_member.HouseholdMember'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectRefusalAudit'])

        # Adding model 'SubjectRefusal'
        db.create_table('bcpp_subject_subjectrefusal', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_member', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household_member.HouseholdMember'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('length_residence', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('refusal_date', self.gf('django.db.models.fields.DateField')()),
            ('why_no_participate', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('why_no_participate_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('subject_refusal_status', self.gf('django.db.models.fields.CharField')(default='REFUSED', max_length=25)),
            ('hiv_test_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('why_no_hivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectRefusal'])

        # Adding model 'SubjectAbsenteeAudit'
        db.create_table('bcpp_subject_subjectabsentee_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsentee', null=True, to=orm['bhp_registration.RegisteredSubject'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsentee', to=orm['bcpp_survey.Survey'])),
            ('subject_absentee_status', self.gf('django.db.models.fields.CharField')(default='absent', max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('household_member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsentee', to=orm['bcpp_household_member.HouseholdMember'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsenteeAudit'])

        # Adding model 'SubjectAbsentee'
        db.create_table('bcpp_subject_subjectabsentee', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_member', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household_member.HouseholdMember'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('subject_absentee_status', self.gf('django.db.models.fields.CharField')(default='absent', max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsentee'])

        # Adding unique constraint on 'SubjectAbsentee', fields ['registered_subject', 'survey']
        db.create_unique('bcpp_subject_subjectabsentee', ['registered_subject_id', 'survey_id'])

        # Adding model 'SubjectAbsenteeReportAudit'
        db.create_table('bcpp_subject_subjectabsenteereport_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('subject_absentee_reason', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsenteereport', to=orm['bcpp_list.SubjectAbsenteeReason'])),
            ('subject_absentee_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('subject_absentee_status', self.gf('django.db.models.fields.CharField')(default='absent', max_length=25)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsenteereport', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsenteeReportAudit'])

        # Adding model 'SubjectAbsenteeReport'
        db.create_table('bcpp_subject_subjectabsenteereport', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('subject_absentee_reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.SubjectAbsenteeReason'])),
            ('subject_absentee_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('subject_absentee_status', self.gf('django.db.models.fields.CharField')(default='absent', max_length=25)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsenteeReport'])

        # Adding model 'SubjectAbsenteeEntryAudit'
        db.create_table('bcpp_subject_subjectabsenteeentry_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_absentee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsenteeentry', to=orm['bcpp_subject.SubjectAbsentee'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subject_absentee_reason', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectabsenteeentry', null=True, to=orm['bcpp_list.SubjectAbsenteeReason'])),
            ('subject_absentee_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsenteeEntryAudit'])

        # Adding model 'SubjectAbsenteeEntry'
        db.create_table('bcpp_subject_subjectabsenteeentry', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('next_appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('next_appt_datetime_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_absentee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_subject.SubjectAbsentee'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subject_absentee_reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_list.SubjectAbsenteeReason'], null=True)),
            ('subject_absentee_reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectAbsenteeEntry'])

        # Adding unique constraint on 'SubjectAbsenteeEntry', fields ['subject_absentee', 'report_datetime']
        db.create_unique('bcpp_subject_subjectabsenteeentry', ['subject_absentee_id', 'report_datetime'])

        # Adding model 'SubjectMovedAudit'
        db.create_table('bcpp_subject_subjectmoved_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectmoved', null=True, to=orm['bhp_registration.RegisteredSubject'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectmoved', to=orm['bcpp_survey.Survey'])),
            ('moved_date', self.gf('django.db.models.fields.DateField')()),
            ('moved_reason', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('moved_reason_other', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
            ('place_moved', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('area_moved', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('household_member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_subjectmoved', to=orm['bcpp_household_member.HouseholdMember'])),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectMovedAudit'])

        # Adding model 'SubjectMoved'
        db.create_table('bcpp_subject_subjectmoved', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('household_member', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_household_member.HouseholdMember'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_survey.Survey'])),
            ('moved_date', self.gf('django.db.models.fields.DateField')()),
            ('moved_reason', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('moved_reason_other', self.gf('django.db.models.fields.TextField')(max_length=250, blank=True)),
            ('place_moved', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('area_moved', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('contact_details', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('bcpp_subject', ['SubjectMoved'])

        # Adding model 'HouseholdCompositionAudit'
        db.create_table('bcpp_subject_householdcomposition_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('housecode', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('physical_add', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('coordinates', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('phone_number', self.gf('django.db.models.fields.IntegerField')(max_length=25)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_householdcomposition', to=orm['bcpp_subject.SubjectVisit'])),
        ))
        db.send_create_signal('bcpp_subject', ['HouseholdCompositionAudit'])

        # Adding model 'HouseholdComposition'
        db.create_table('bcpp_subject_householdcomposition', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_subject.SubjectVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 10, 0, 0))),
            ('housecode', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('physical_add', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('coordinates', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('phone_number', self.gf('django.db.models.fields.IntegerField')(max_length=25)),
        ))
        db.send_create_signal('bcpp_subject', ['HouseholdComposition'])

        # Adding model 'RespondentAudit'
        db.create_table('bcpp_subject_respondent_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('relation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('nights_outside', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('household_composition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_respondent', to=orm['bcpp_subject.HouseholdComposition'])),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bcpp_subject', ['RespondentAudit'])

        # Adding model 'Respondent'
        db.create_table('bcpp_subject_respondent', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('relation_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('present', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('nights_outside', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('household_composition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcpp_subject.HouseholdComposition'])),
        ))
        db.send_create_signal('bcpp_subject', ['Respondent'])


    def backwards(self, orm):
        # Removing unique constraint on 'SubjectAbsenteeEntry', fields ['subject_absentee', 'report_datetime']
        db.delete_unique('bcpp_subject_subjectabsenteeentry', ['subject_absentee_id', 'report_datetime'])

        # Removing unique constraint on 'SubjectAbsentee', fields ['registered_subject', 'survey']
        db.delete_unique('bcpp_subject_subjectabsentee', ['registered_subject_id', 'survey_id'])

        # Deleting model 'SubjectOffStudyAudit'
        db.delete_table('bcpp_subject_subjectoffstudy_audit')

        # Deleting model 'SubjectOffStudy'
        db.delete_table('bcpp_subject_subjectoffstudy')

        # Deleting model 'SubjectConsentAudit'
        db.delete_table('bcpp_subject_subjectconsent_audit')

        # Deleting model 'SubjectConsent'
        db.delete_table('bcpp_subject_subjectconsent')

        # Deleting model 'SubjectVisitAudit'
        db.delete_table('bcpp_subject_subjectvisit_audit')

        # Deleting model 'SubjectVisit'
        db.delete_table('bcpp_subject_subjectvisit')

        # Deleting model 'SubjectLocatorAudit'
        db.delete_table('bcpp_subject_subjectlocator_audit')

        # Deleting model 'SubjectLocator'
        db.delete_table('bcpp_subject_subjectlocator')

        # Deleting model 'SubjectDeathAudit'
        db.delete_table('bcpp_subject_subjectdeath_audit')

        # Deleting model 'SubjectDeath'
        db.delete_table('bcpp_subject_subjectdeath')

        # Deleting model 'RecentPartnerAudit'
        db.delete_table('bcpp_subject_recentpartner_audit')

        # Deleting model 'RecentPartner'
        db.delete_table('bcpp_subject_recentpartner')

        # Deleting model 'SecondPartnerAudit'
        db.delete_table('bcpp_subject_secondpartner_audit')

        # Deleting model 'SecondPartner'
        db.delete_table('bcpp_subject_secondpartner')

        # Deleting model 'ThirdPartnerAudit'
        db.delete_table('bcpp_subject_thirdpartner_audit')

        # Deleting model 'ThirdPartner'
        db.delete_table('bcpp_subject_thirdpartner')

        # Deleting model 'QualityOfLifeAudit'
        db.delete_table('bcpp_subject_qualityoflife_audit')

        # Deleting model 'QualityOfLife'
        db.delete_table('bcpp_subject_qualityoflife')

        # Deleting model 'ResourceUtilizationAudit'
        db.delete_table('bcpp_subject_resourceutilization_audit')

        # Deleting model 'ResourceUtilization'
        db.delete_table('bcpp_subject_resourceutilization')

        # Deleting model 'OutpatientCareAudit'
        db.delete_table('bcpp_subject_outpatientcare_audit')

        # Deleting model 'OutpatientCare'
        db.delete_table('bcpp_subject_outpatientcare')

        # Deleting model 'HospitalAdmissionAudit'
        db.delete_table('bcpp_subject_hospitaladmission_audit')

        # Deleting model 'HospitalAdmission'
        db.delete_table('bcpp_subject_hospitaladmission')

        # Deleting model 'HivHealthCareCostsAudit'
        db.delete_table('bcpp_subject_hivhealthcarecosts_audit')

        # Deleting model 'HivHealthCareCosts'
        db.delete_table('bcpp_subject_hivhealthcarecosts')

        # Deleting model 'LabourMarketWagesAudit'
        db.delete_table('bcpp_subject_labourmarketwages_audit')

        # Deleting model 'LabourMarketWages'
        db.delete_table('bcpp_subject_labourmarketwages')

        # Deleting model 'GrantAudit'
        db.delete_table('bcpp_subject_grant_audit')

        # Deleting model 'Grant'
        db.delete_table('bcpp_subject_grant')

        # Deleting model 'BaselineHouseholdSurveyAudit'
        db.delete_table('bcpp_subject_baselinehouseholdsurvey_audit')

        # Deleting model 'BaselineHouseholdSurvey'
        db.delete_table('bcpp_subject_baselinehouseholdsurvey')

        # Removing M2M table for field electrical_appliances on 'BaselineHouseholdSurvey'
        db.delete_table('bcpp_subject_baselinehouseholdsurvey_electrical_appliances')

        # Removing M2M table for field transport_mode on 'BaselineHouseholdSurvey'
        db.delete_table('bcpp_subject_baselinehouseholdsurvey_transport_mode')

        # Deleting model 'CeaEnrolmentChecklistAudit'
        db.delete_table('bcpp_subject_ceaenrolmentchecklist_audit')

        # Deleting model 'CeaEnrolmentChecklist'
        db.delete_table('bcpp_subject_ceaenrolmentchecklist')

        # Deleting model 'CsEnrolmentChecklistAudit'
        db.delete_table('bcpp_subject_csenrolmentchecklist_audit')

        # Deleting model 'CsEnrolmentChecklist'
        db.delete_table('bcpp_subject_csenrolmentchecklist')

        # Deleting model 'ResidencyMobilityAudit'
        db.delete_table('bcpp_subject_residencymobility_audit')

        # Deleting model 'ResidencyMobility'
        db.delete_table('bcpp_subject_residencymobility')

        # Deleting model 'DemographicsAudit'
        db.delete_table('bcpp_subject_demographics_audit')

        # Deleting model 'Demographics'
        db.delete_table('bcpp_subject_demographics')

        # Removing M2M table for field religion on 'Demographics'
        db.delete_table('bcpp_subject_demographics_religion')

        # Removing M2M table for field live_with on 'Demographics'
        db.delete_table('bcpp_subject_demographics_live_with')

        # Deleting model 'CommunityEngagementAudit'
        db.delete_table('bcpp_subject_communityengagement_audit')

        # Deleting model 'CommunityEngagement'
        db.delete_table('bcpp_subject_communityengagement')

        # Removing M2M table for field problems_engagement on 'CommunityEngagement'
        db.delete_table('bcpp_subject_communityengagement_problems_engagement')

        # Deleting model 'EducationAudit'
        db.delete_table('bcpp_subject_education_audit')

        # Deleting model 'Education'
        db.delete_table('bcpp_subject_education')

        # Deleting model 'HivTestingHistoryAudit'
        db.delete_table('bcpp_subject_hivtestinghistory_audit')

        # Deleting model 'HivTestingHistory'
        db.delete_table('bcpp_subject_hivtestinghistory')

        # Deleting model 'HivTestReviewAudit'
        db.delete_table('bcpp_subject_hivtestreview_audit')

        # Deleting model 'HivTestReview'
        db.delete_table('bcpp_subject_hivtestreview')

        # Deleting model 'HivTestedAudit'
        db.delete_table('bcpp_subject_hivtested_audit')

        # Deleting model 'HivTested'
        db.delete_table('bcpp_subject_hivtested')

        # Deleting model 'HivUntestedAudit'
        db.delete_table('bcpp_subject_hivuntested_audit')

        # Deleting model 'HivUntested'
        db.delete_table('bcpp_subject_hivuntested')

        # Deleting model 'FutureHivTestingAudit'
        db.delete_table('bcpp_subject_futurehivtesting_audit')

        # Deleting model 'FutureHivTesting'
        db.delete_table('bcpp_subject_futurehivtesting')

        # Deleting model 'SexualBehaviourAudit'
        db.delete_table('bcpp_subject_sexualbehaviour_audit')

        # Deleting model 'SexualBehaviour'
        db.delete_table('bcpp_subject_sexualbehaviour')

        # Deleting model 'MonthsRecentPartnerAudit'
        db.delete_table('bcpp_subject_monthsrecentpartner_audit')

        # Deleting model 'MonthsRecentPartner'
        db.delete_table('bcpp_subject_monthsrecentpartner')

        # Removing M2M table for field first_partner_live on 'MonthsRecentPartner'
        db.delete_table('bcpp_subject_monthsrecentpartner_first_partner_live')

        # Deleting model 'MonthsSecondPartnerAudit'
        db.delete_table('bcpp_subject_monthssecondpartner_audit')

        # Deleting model 'MonthsSecondPartner'
        db.delete_table('bcpp_subject_monthssecondpartner')

        # Removing M2M table for field first_partner_live on 'MonthsSecondPartner'
        db.delete_table('bcpp_subject_monthssecondpartner_first_partner_live')

        # Deleting model 'MonthsThirdPartnerAudit'
        db.delete_table('bcpp_subject_monthsthirdpartner_audit')

        # Deleting model 'MonthsThirdPartner'
        db.delete_table('bcpp_subject_monthsthirdpartner')

        # Removing M2M table for field first_partner_live on 'MonthsThirdPartner'
        db.delete_table('bcpp_subject_monthsthirdpartner_first_partner_live')

        # Deleting model 'HivCareAdherenceAudit'
        db.delete_table('bcpp_subject_hivcareadherence_audit')

        # Deleting model 'HivCareAdherence'
        db.delete_table('bcpp_subject_hivcareadherence')

        # Deleting model 'HivMedicalCareAudit'
        db.delete_table('bcpp_subject_hivmedicalcare_audit')

        # Deleting model 'HivMedicalCare'
        db.delete_table('bcpp_subject_hivmedicalcare')

        # Deleting model 'CircumcisionAudit'
        db.delete_table('bcpp_subject_circumcision_audit')

        # Deleting model 'Circumcision'
        db.delete_table('bcpp_subject_circumcision')

        # Deleting model 'CircumcisedAudit'
        db.delete_table('bcpp_subject_circumcised_audit')

        # Deleting model 'Circumcised'
        db.delete_table('bcpp_subject_circumcised')

        # Removing M2M table for field health_benefits_smc on 'Circumcised'
        db.delete_table('bcpp_subject_circumcised_health_benefits_smc')

        # Deleting model 'UncircumcisedAudit'
        db.delete_table('bcpp_subject_uncircumcised_audit')

        # Deleting model 'Uncircumcised'
        db.delete_table('bcpp_subject_uncircumcised')

        # Removing M2M table for field health_benefits_smc on 'Uncircumcised'
        db.delete_table('bcpp_subject_uncircumcised_health_benefits_smc')

        # Deleting model 'ReproductiveHealthAudit'
        db.delete_table('bcpp_subject_reproductivehealth_audit')

        # Deleting model 'ReproductiveHealth'
        db.delete_table('bcpp_subject_reproductivehealth')

        # Deleting model 'MedicalDiagnosesAudit'
        db.delete_table('bcpp_subject_medicaldiagnoses_audit')

        # Deleting model 'MedicalDiagnoses'
        db.delete_table('bcpp_subject_medicaldiagnoses')

        # Removing M2M table for field diagnoses on 'MedicalDiagnoses'
        db.delete_table('bcpp_subject_medicaldiagnoses_diagnoses')

        # Deleting model 'HeartAttackAudit'
        db.delete_table('bcpp_subject_heartattack_audit')

        # Deleting model 'HeartAttack'
        db.delete_table('bcpp_subject_heartattack')

        # Removing M2M table for field dx_heart_attack on 'HeartAttack'
        db.delete_table('bcpp_subject_heartattack_dx_heart_attack')

        # Deleting model 'CancerAudit'
        db.delete_table('bcpp_subject_cancer_audit')

        # Deleting model 'Cancer'
        db.delete_table('bcpp_subject_cancer')

        # Deleting model 'TubercolosisAudit'
        db.delete_table('bcpp_subject_tubercolosis_audit')

        # Deleting model 'Tubercolosis'
        db.delete_table('bcpp_subject_tubercolosis')

        # Deleting model 'SubstanceUseAudit'
        db.delete_table('bcpp_subject_substanceuse_audit')

        # Deleting model 'SubstanceUse'
        db.delete_table('bcpp_subject_substanceuse')

        # Deleting model 'StigmaAudit'
        db.delete_table('bcpp_subject_stigma_audit')

        # Deleting model 'Stigma'
        db.delete_table('bcpp_subject_stigma')

        # Deleting model 'StigmaOpinionAudit'
        db.delete_table('bcpp_subject_stigmaopinion_audit')

        # Deleting model 'StigmaOpinion'
        db.delete_table('bcpp_subject_stigmaopinion')

        # Deleting model 'PositiveParticipantAudit'
        db.delete_table('bcpp_subject_positiveparticipant_audit')

        # Deleting model 'PositiveParticipant'
        db.delete_table('bcpp_subject_positiveparticipant')

        # Deleting model 'AccessToCareAudit'
        db.delete_table('bcpp_subject_accesstocare_audit')

        # Deleting model 'AccessToCare'
        db.delete_table('bcpp_subject_accesstocare')

        # Removing M2M table for field medical_care_access on 'AccessToCare'
        db.delete_table('bcpp_subject_accesstocare_medical_care_access')

        # Deleting model 'TodaysHivResultAudit'
        db.delete_table('bcpp_subject_todayshivresult_audit')

        # Deleting model 'TodaysHivResult'
        db.delete_table('bcpp_subject_todayshivresult')

        # Deleting model 'PregnancyAudit'
        db.delete_table('bcpp_subject_pregnancy_audit')

        # Deleting model 'Pregnancy'
        db.delete_table('bcpp_subject_pregnancy')

        # Removing M2M table for field family_planning on 'Pregnancy'
        db.delete_table('bcpp_subject_pregnancy_family_planning')

        # Deleting model 'HivResultDocumentationAudit'
        db.delete_table('bcpp_subject_hivresultdocumentation_audit')

        # Deleting model 'HivResultDocumentation'
        db.delete_table('bcpp_subject_hivresultdocumentation')

        # Deleting model 'SubjectRefusalAudit'
        db.delete_table('bcpp_subject_subjectrefusal_audit')

        # Deleting model 'SubjectRefusal'
        db.delete_table('bcpp_subject_subjectrefusal')

        # Deleting model 'SubjectAbsenteeAudit'
        db.delete_table('bcpp_subject_subjectabsentee_audit')

        # Deleting model 'SubjectAbsentee'
        db.delete_table('bcpp_subject_subjectabsentee')

        # Deleting model 'SubjectAbsenteeReportAudit'
        db.delete_table('bcpp_subject_subjectabsenteereport_audit')

        # Deleting model 'SubjectAbsenteeReport'
        db.delete_table('bcpp_subject_subjectabsenteereport')

        # Deleting model 'SubjectAbsenteeEntryAudit'
        db.delete_table('bcpp_subject_subjectabsenteeentry_audit')

        # Deleting model 'SubjectAbsenteeEntry'
        db.delete_table('bcpp_subject_subjectabsenteeentry')

        # Deleting model 'SubjectMovedAudit'
        db.delete_table('bcpp_subject_subjectmoved_audit')

        # Deleting model 'SubjectMoved'
        db.delete_table('bcpp_subject_subjectmoved')

        # Deleting model 'HouseholdCompositionAudit'
        db.delete_table('bcpp_subject_householdcomposition_audit')

        # Deleting model 'HouseholdComposition'
        db.delete_table('bcpp_subject_householdcomposition')

        # Deleting model 'RespondentAudit'
        db.delete_table('bcpp_subject_respondent_audit')

        # Deleting model 'Respondent'
        db.delete_table('bcpp_subject_respondent')


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
        'bcpp_household_member.householdmember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdMember'},
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.ContactLog']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
        'bcpp_list.circumcisionbenefits': {
            'Meta': {'object_name': 'CircumcisionBenefits'},
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
        'bcpp_list.diagnoses': {
            'Meta': {'object_name': 'Diagnoses'},
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
        'bcpp_list.electricalappliances': {
            'Meta': {'object_name': 'ElectricalAppliances'},
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
        'bcpp_list.familyplanning': {
            'Meta': {'object_name': 'FamilyPlanning'},
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
        'bcpp_list.heartdisease': {
            'Meta': {'object_name': 'HeartDisease'},
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
        'bcpp_list.livewith': {
            'Meta': {'object_name': 'LiveWith'},
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
        'bcpp_list.medicalcareaccess': {
            'Meta': {'object_name': 'MedicalCareAccess'},
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
        'bcpp_list.neighbourhoodproblems': {
            'Meta': {'object_name': 'NeighbourhoodProblems'},
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
        'bcpp_list.partnerresidency': {
            'Meta': {'object_name': 'PartnerResidency'},
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
        'bcpp_list.religion': {
            'Meta': {'object_name': 'Religion'},
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
        'bcpp_list.subjectabsenteereason': {
            'Meta': {'object_name': 'SubjectAbsenteeReason'},
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
        'bcpp_list.transportmode': {
            'Meta': {'object_name': 'TransportMode'},
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
        'bcpp_subject.accesstocare': {
            'Meta': {'object_name': 'AccessToCare'},
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_care_access': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.MedicalCareAccess']", 'symmetrical': 'False'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.accesstocareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'AccessToCareAudit', 'db_table': "'bcpp_subject_accesstocare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_accesstocare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.baselinehouseholdsurvey': {
            'Meta': {'object_name': 'BaselineHouseholdSurvey'},
            'cattle_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'electrical_appliances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.ElectricalAppliances']", 'null': 'True', 'blank': 'True'}),
            'energy_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'energy_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'flooring_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'flooring_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'goats_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'transport_mode': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.TransportMode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.baselinehouseholdsurveyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'BaselineHouseholdSurveyAudit', 'db_table': "'bcpp_subject_baselinehouseholdsurvey_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cattle_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'energy_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'energy_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'flooring_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'flooring_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'goats_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_baselinehouseholdsurvey'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.cancer': {
            'Meta': {'object_name': 'Cancer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.canceraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CancerAudit', 'db_table': "'bcpp_subject_cancer_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_cancer'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.ceaenrolmentchecklist': {
            'Meta': {'object_name': 'CeaEnrolmentChecklist'},
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrolment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.ceaenrolmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CeaEnrolmentChecklistAudit', 'db_table': "'bcpp_subject_ceaenrolmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrolment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_ceaenrolmentchecklist'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcised': {
            'Meta': {'object_name': 'Circumcised'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.CircumcisionBenefits']", 'max_length': '25', 'symmetrical': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.circumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisedAudit', 'db_table': "'bcpp_subject_circumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.circumcision': {
            'Meta': {'object_name': 'Circumcision'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcisionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisionAudit', 'db_table': "'bcpp_subject_circumcision_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcision'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.communityengagement': {
            'Meta': {'object_name': 'CommunityEngagement'},
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.NeighbourhoodProblems']", 'symmetrical': 'False'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.communityengagementaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CommunityEngagementAudit', 'db_table': "'bcpp_subject_communityengagement_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_communityengagement'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.csenrolmentchecklist': {
            'Meta': {'object_name': 'CsEnrolmentChecklist'},
            'census_number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_consent_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'date_guardian_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'date_minor_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.csenrolmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CsEnrolmentChecklistAudit', 'db_table': "'bcpp_subject_csenrolmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'census_number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_consent_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'date_guardian_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'date_minor_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_csenrolmentchecklist'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'husband_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'live_with': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.LiveWith']", 'symmetrical': 'False'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'religion': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.Religion']", 'symmetrical': 'False'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.demographicsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'DemographicsAudit', 'db_table': "'bcpp_subject_demographics_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'husband_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_demographics'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.education': {
            'Meta': {'object_name': 'Education'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_unemployed': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'working': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'bcpp_subject.educationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'EducationAudit', 'db_table': "'bcpp_subject_education_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_unemployed': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_education'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'working': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'bcpp_subject.futurehivtesting': {
            'Meta': {'object_name': 'FutureHivTesting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.futurehivtestingaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'FutureHivTestingAudit', 'db_table': "'bcpp_subject_futurehivtesting_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_futurehivtesting'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grant': {
            'Meta': {'object_name': 'Grant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'GrantAudit', 'db_table': "'bcpp_subject_grant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_grant'", 'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.heartattack': {
            'Meta': {'object_name': 'HeartAttack'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {}),
            'dx_heart_attack': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.HeartDisease']", 'symmetrical': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.heartattackaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HeartAttackAudit', 'db_table': "'bcpp_subject_heartattack_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_heartattack'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivcareadherence': {
            'Meta': {'object_name': 'HivCareAdherence'},
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivcareadherenceaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivCareAdherenceAudit', 'db_table': "'bcpp_subject_hivcareadherence_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivcareadherence'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivhealthcarecosts': {
            'Meta': {'object_name': 'HivHealthCareCosts'},
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivhealthcarecostsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivHealthCareCostsAudit', 'db_table': "'bcpp_subject_hivhealthcarecosts_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivhealthcarecosts'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcare': {
            'Meta': {'object_name': 'HivMedicalCare'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivMedicalCareAudit', 'db_table': "'bcpp_subject_hivmedicalcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivmedicalcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivresultdocumentation': {
            'Meta': {'object_name': 'HivResultDocumentation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'result_date': ('django.db.models.fields.DateField', [], {}),
            'result_doc_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'result_recorded': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivresultdocumentationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivResultDocumentationAudit', 'db_table': "'bcpp_subject_hivresultdocumentation_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'result_date': ('django.db.models.fields.DateField', [], {}),
            'result_doc_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'result_recorded': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivresultdocumentation'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivtested': {
            'Meta': {'object_name': 'HivTested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestedAudit', 'db_table': "'bcpp_subject_hivtested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestinghistory': {
            'Meta': {'object_name': 'HivTestingHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_record': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestinghistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestingHistoryAudit', 'db_table': "'bcpp_subject_hivtestinghistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_record': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestinghistory'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestreview': {
            'Meta': {'object_name': 'HivTestReview'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivtestreviewaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestReviewAudit', 'db_table': "'bcpp_subject_hivtestreview_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestreview'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivuntested': {
            'Meta': {'object_name': 'HivUntested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivuntestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivUntestedAudit', 'db_table': "'bcpp_subject_hivuntested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivuntested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hospitaladmission': {
            'Meta': {'object_name': 'HospitalAdmission'},
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hospitaladmissionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HospitalAdmissionAudit', 'db_table': "'bcpp_subject_hospitaladmission_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hospitaladmission'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.householdcomposition': {
            'Meta': {'object_name': 'HouseholdComposition'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'housecode': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {'max_length': '25'}),
            'physical_add': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.householdcompositionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdCompositionAudit', 'db_table': "'bcpp_subject_householdcomposition_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'housecode': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {'max_length': '25'}),
            'physical_add': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdcomposition'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.labourmarketwages': {
            'Meta': {'object_name': 'LabourMarketWages'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.labourmarketwagesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LabourMarketWagesAudit', 'db_table': "'bcpp_subject_labourmarketwages_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_labourmarketwages'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.medicaldiagnoses': {
            'Meta': {'object_name': 'MedicalDiagnoses'},
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'diagnoses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.Diagnoses']", 'symmetrical': 'False'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sti': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.medicaldiagnosesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MedicalDiagnosesAudit', 'db_table': "'bcpp_subject_medicaldiagnoses_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sti': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_medicaldiagnoses'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartner': {
            'Meta': {'object_name': 'MonthsRecentPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsRecentPartnerAudit', 'db_table': "'bcpp_subject_monthsrecentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsrecentpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartner': {
            'Meta': {'object_name': 'MonthsSecondPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsSecondPartnerAudit', 'db_table': "'bcpp_subject_monthssecondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthssecondpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartner': {
            'Meta': {'object_name': 'MonthsThirdPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsThirdPartnerAudit', 'db_table': "'bcpp_subject_monthsthirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsthirdpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.outpatientcare': {
            'Meta': {'object_name': 'OutpatientCare'},
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.outpatientcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'OutpatientCareAudit', 'db_table': "'bcpp_subject_outpatientcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_outpatientcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.positiveparticipant': {
            'Meta': {'object_name': 'PositiveParticipant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.positiveparticipantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PositiveParticipantAudit', 'db_table': "'bcpp_subject_positiveparticipant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_positiveparticipant'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.pregnancy': {
            'Meta': {'object_name': 'Pregnancy'},
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_planning': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.FamilyPlanning']", 'symmetrical': 'False'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {}),
            'lnmp': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'bcpp_subject.pregnancyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PregnancyAudit', 'db_table': "'bcpp_subject_pregnancy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {}),
            'lnmp': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_pregnancy'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'bcpp_subject.qualityoflife': {
            'Meta': {'object_name': 'QualityOfLife'},
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.qualityoflifeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'QualityOfLifeAudit', 'db_table': "'bcpp_subject_qualityoflife_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_qualityoflife'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.recentpartner': {
            'Meta': {'object_name': 'RecentPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.recentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'RecentPartnerAudit', 'db_table': "'bcpp_subject_recentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_recentpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.reproductivehealth': {
            'Meta': {'object_name': 'ReproductiveHealth'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'menopause': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.reproductivehealthaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReproductiveHealthAudit', 'db_table': "'bcpp_subject_reproductivehealth_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'menopause': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_reproductivehealth'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.residencymobility': {
            'Meta': {'object_name': 'ResidencyMobility'},
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'forteen_nights': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.residencymobilityaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResidencyMobilityAudit', 'db_table': "'bcpp_subject_residencymobility_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'forteen_nights': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_residencymobility'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilization': {
            'Meta': {'object_name': 'ResourceUtilization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilizationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResourceUtilizationAudit', 'db_table': "'bcpp_subject_resourceutilization_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_resourceutilization'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.respondent': {
            'Meta': {'object_name': 'Respondent'},
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_composition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.HouseholdComposition']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_outside': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.respondentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'RespondentAudit', 'db_table': "'bcpp_subject_respondent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_composition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_respondent'", 'to': "orm['bcpp_subject.HouseholdComposition']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_outside': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.secondpartner': {
            'Meta': {'object_name': 'SecondPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.secondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SecondPartnerAudit', 'db_table': "'bcpp_subject_secondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_secondpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviour': {
            'Meta': {'object_name': 'SexualBehaviour'},
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviouraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SexualBehaviourAudit', 'db_table': "'bcpp_subject_sexualbehaviour_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_sexualbehaviour'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigma': {
            'Meta': {'object_name': 'Stigma'},
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaAudit', 'db_table': "'bcpp_subject_stigma_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigma'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinion': {
            'Meta': {'object_name': 'StigmaOpinion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaOpinionAudit', 'db_table': "'bcpp_subject_stigmaopinion_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigmaopinion'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsentee': {
            'Meta': {'unique_together': "(('registered_subject', 'survey'),)", 'object_name': 'SubjectAbsentee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeAudit', 'db_table': "'bcpp_subject_subjectabsentee_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeentry': {
            'Meta': {'unique_together': "(('subject_absentee', 'report_datetime'),)", 'object_name': 'SubjectAbsenteeEntry'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_absentee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectAbsentee']"}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SubjectAbsenteeReason']", 'null': 'True'}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeentryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeEntryAudit', 'db_table': "'bcpp_subject_subjectabsenteeentry_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_absentee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteeentry'", 'to': "orm['bcpp_subject.SubjectAbsentee']"}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteeentry'", 'null': 'True', 'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteereport': {
            'Meta': {'object_name': 'SubjectAbsenteeReport'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteereportaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeReportAudit', 'db_table': "'bcpp_subject_subjectabsenteereport_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteereport'", 'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteereport'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectconsent': {
            'Meta': {'object_name': 'SubjectConsent'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectconsentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectConsentAudit', 'db_table': "'bcpp_subject_subjectconsent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectdeath': {
            'Meta': {'object_name': 'SubjectDeath'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathReasonHospitalized']", 'null': 'True', 'blank': 'True'}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectdeathaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectDeathAudit', 'db_table': "'bcpp_subject_subjectdeath_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_adverse.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_adverse.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_audit_subjectdeath'", 'null': 'True', 'to': "orm['bhp_adverse.DeathReasonHospitalized']"}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocator': {
            'Meta': {'object_name': 'SubjectLocator'},
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'null': 'True'}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocatoraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectLocatorAudit', 'db_table': "'bcpp_subject_subjectlocator_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectmoved': {
            'Meta': {'ordering': "['household_member']", 'object_name': 'SubjectMoved'},
            'area_moved': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'moved_date': ('django.db.models.fields.DateField', [], {}),
            'moved_reason': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'moved_reason_other': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'place_moved': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectmovedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectMovedAudit', 'db_table': "'bcpp_subject_subjectmoved_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'area_moved': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'moved_date': ('django.db.models.fields.DateField', [], {}),
            'moved_reason': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'moved_reason_other': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'place_moved': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudy': {
            'Meta': {'object_name': 'SubjectOffStudy'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectOffStudyAudit', 'db_table': "'bcpp_subject_subjectoffstudy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectoffstudy'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectrefusal': {
            'Meta': {'ordering': "['household_member']", 'object_name': 'SubjectRefusal'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'refusal_date': ('django.db.models.fields.DateField', [], {}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_refusal_status': ('django.db.models.fields.CharField', [], {'default': "'REFUSED'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'why_no_participate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'why_no_participate_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.subjectrefusalaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectRefusalAudit', 'db_table': "'bcpp_subject_subjectrefusal_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'refusal_date': ('django.db.models.fields.DateField', [], {}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_refusal_status': ('django.db.models.fields.CharField', [], {'default': "'REFUSED'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'why_no_participate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'why_no_participate_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.subjectvisit': {
            'Meta': {'object_name': 'SubjectVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectvisitaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectVisitAudit', 'db_table': "'bcpp_subject_subjectvisit_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectvisit'", 'to': "orm['bhp_appointment.Appointment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuse': {
            'Meta': {'object_name': 'SubstanceUse'},
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuseaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubstanceUseAudit', 'db_table': "'bcpp_subject_substanceuse_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_substanceuse'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.thirdpartner': {
            'Meta': {'object_name': 'ThirdPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.thirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ThirdPartnerAudit', 'db_table': "'bcpp_subject_thirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_thirdpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.todayshivresult': {
            'Meta': {'object_name': 'TodaysHivResult'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.todayshivresultaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TodaysHivResultAudit', 'db_table': "'bcpp_subject_todayshivresult_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_todayshivresult'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.tubercolosis': {
            'Meta': {'object_name': 'Tubercolosis'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.tubercolosisaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TubercolosisAudit', 'db_table': "'bcpp_subject_tubercolosis_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_tubercolosis'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcised': {
            'Meta': {'object_name': 'Uncircumcised'},
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_week': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_year': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.CircumcisionBenefits']", 'max_length': '25', 'symmetrical': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'UncircumcisedAudit', 'db_table': "'bcpp_subject_uncircumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_week': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_year': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 10, 0, 0)'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_uncircumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
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
        },
        'bhp_adverse.deathcausecategory': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathCauseCategory'},
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
        'bhp_adverse.deathcauseinfo': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathCauseInfo'},
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
        'bhp_adverse.deathreasonhospitalized': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathReasonHospitalized'},
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
        'bhp_appointment.appointment': {
            'Meta': {'ordering': "['registered_subject', 'appt_datetime']", 'unique_together': "(('registered_subject', 'visit_definition', 'visit_instance'),)", 'object_name': 'Appointment'},
            'appt_close_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25', 'db_index': 'True'}),
            'appt_type': ('django.db.models.fields.CharField', [], {'default': "'clinic'", 'max_length': '20'}),
            'best_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dashboard_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'timepoint_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['bhp_visit.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'bhp_content_type_map.contenttypemap': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap', 'db_table': "'bhp_common_contenttypemap'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials'),)", 'object_name': 'RegisteredSubject'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_visit.membershipform': {
            'Meta': {'object_name': 'MembershipForm'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '25', 'null': 'True'}),
            'content_type_map': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'bhp_visit.schedulegroup': {
            'Meta': {'ordering': "['group_name']", 'object_name': 'ScheduleGroup'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'grouping_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'membership_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_visit.MembershipForm']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_visit.visitdefinition': {
            'Meta': {'ordering': "['code', 'time_point']", 'object_name': 'VisitDefinition'},
            'base_interval': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'base_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'lower_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lower_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'schedule_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bhp_visit.ScheduleGroup']", 'null': 'True', 'blank': 'True'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_index': 'True'}),
            'upper_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upper_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_tracking_content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bcpp_subject']
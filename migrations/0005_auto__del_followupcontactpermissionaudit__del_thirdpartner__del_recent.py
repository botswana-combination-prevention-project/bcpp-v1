# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FollowupContactPermissionAudit'
        db.delete_table('bcpp_htc_followupcontactpermission_audit')

        # Deleting model 'ThirdPartner'
        db.delete_table('bcpp_htc_thirdpartner')

        # Deleting model 'RecentPartnerAudit'
        db.delete_table('bcpp_htc_recentpartner_audit')

        # Deleting model 'HivTestingCounselingAudit'
        db.delete_table('bcpp_htc_hivtestingcounseling_audit')

        # Deleting model 'SecondPartner'
        db.delete_table('bcpp_htc_secondpartner')

        # Deleting model 'SecondPartnerAudit'
        db.delete_table('bcpp_htc_secondpartner_audit')

        # Deleting model 'ThirdPartnerAudit'
        db.delete_table('bcpp_htc_thirdpartner_audit')

        # Deleting model 'HivTestingCounseling'
        db.delete_table('bcpp_htc_hivtestingcounseling')

        # Deleting model 'FollowupContactPermission'
        db.delete_table('bcpp_htc_followupcontactpermission')

        # Deleting model 'RecentPartner'
        db.delete_table('bcpp_htc_recentpartner')

        # Adding model 'Cd4Test'
        db.create_table('bcpp_htc_cd4test', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('cd4_test_date', self.gf('django.db.models.fields.DateField')()),
            ('cd4_result', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('referral_clinic', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('bcpp_htc', ['Cd4Test'])

        # Adding model 'HtcSecondPartnerAudit'
        db.create_table('bcpp_htc_htcsecondpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('second_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_htcsecondpartner', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['HtcSecondPartnerAudit'])

        # Adding model 'HivTestingConsentAudit'
        db.create_table('bcpp_htc_hivtestingconsent_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('testing_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reason_not_testing', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivtestingconsent', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['HivTestingConsentAudit'])

        # Adding model 'HtcRecentPartnerAudit'
        db.create_table('bcpp_htc_htcrecentpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('recent_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_htcrecentpartner', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['HtcRecentPartnerAudit'])

        # Adding model 'CircumcisionAppointmentAudit'
        db.create_table('bcpp_htc_circumcisionappointment_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('circumcision_ap', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_ap_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_circumcisionappointment', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['CircumcisionAppointmentAudit'])

        # Adding model 'PregnantFollowup'
        db.create_table('bcpp_htc_pregnantfollowup', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['PregnantFollowup'])

        # Adding model 'HtcSecondPartner'
        db.create_table('bcpp_htc_htcsecondpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('second_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('bcpp_htc', ['HtcSecondPartner'])

        # Adding model 'HivResult'
        db.create_table('bcpp_htc_hivresult', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('todays_result', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('couples_testing', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('partner_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('symptoms', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('family_tb', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('bcpp_htc', ['HivResult'])

        # Adding model 'Referral'
        db.create_table('bcpp_htc_referral', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
        ))
        db.send_create_signal('bcpp_htc', ['Referral'])

        # Adding M2M table for field referred_for on 'Referral'
        m2m_table_name = db.shorten_name('bcpp_htc_referral_referred_for')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('referral', models.ForeignKey(orm['bcpp_htc.referral'], null=False)),
            ('referredfor', models.ForeignKey(orm['bcpp_list.referredfor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['referral_id', 'referredfor_id'])

        # Adding M2M table for field referred_to on 'Referral'
        m2m_table_name = db.shorten_name('bcpp_htc_referral_referred_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('referral', models.ForeignKey(orm['bcpp_htc.referral'], null=False)),
            ('referredto', models.ForeignKey(orm['bcpp_list.referredto'], null=False))
        ))
        db.create_unique(m2m_table_name, ['referral_id', 'referredto_id'])

        # Adding model 'HtcRecentPartner'
        db.create_table('bcpp_htc_htcrecentpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('recent_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('bcpp_htc', ['HtcRecentPartner'])

        # Adding model 'HtcThirdPartnerAudit'
        db.create_table('bcpp_htc_htcthirdpartner_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('third_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_htcthirdpartner', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['HtcThirdPartnerAudit'])

        # Adding model 'HivTestingConsent'
        db.create_table('bcpp_htc_hivtestingconsent', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('testing_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reason_not_testing', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_htc', ['HivTestingConsent'])

        # Adding model 'Cd4TestAudit'
        db.create_table('bcpp_htc_cd4test_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('cd4_test_date', self.gf('django.db.models.fields.DateField')()),
            ('cd4_result', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('referral_clinic', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')()),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_cd4test', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['Cd4TestAudit'])

        # Adding model 'MaleFollowupAudit'
        db.create_table('bcpp_htc_malefollowup_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_malefollowup', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['MaleFollowupAudit'])

        # Adding model 'HtcThirdPartner'
        db.create_table('bcpp_htc_htcthirdpartner', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('third_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal('bcpp_htc', ['HtcThirdPartner'])

        # Adding model 'PositiveFollowupAudit'
        db.create_table('bcpp_htc_positivefollowup_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_positivefollowup', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['PositiveFollowupAudit'])

        # Adding model 'CircumcisionAppointment'
        db.create_table('bcpp_htc_circumcisionappointment', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('circumcision_ap', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_ap_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('bcpp_htc', ['CircumcisionAppointment'])

        # Adding model 'PregnantFollowupAudit'
        db.create_table('bcpp_htc_pregnantfollowup_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_pregnantfollowup', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['PregnantFollowupAudit'])

        # Adding model 'HivResultAudit'
        db.create_table('bcpp_htc_hivresult_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('todays_result', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('couples_testing', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('partner_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('symptoms', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('family_tb', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivresult', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['HivResultAudit'])

        # Adding model 'MaleFollowup'
        db.create_table('bcpp_htc_malefollowup', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['MaleFollowup'])

        # Adding model 'PositiveFollowup'
        db.create_table('bcpp_htc_positivefollowup', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('contact_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['PositiveFollowup'])

        # Adding model 'ReferralAudit'
        db.create_table('bcpp_htc_referral_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='silverapple-2.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0))),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_referral', to=orm['bcpp_htc.HtcVisit'])),
        ))
        db.send_create_signal('bcpp_htc', ['ReferralAudit'])

        # Adding field 'HtcRegistration.subject_identifier'
        db.add_column('bcpp_htc_htcregistration', 'subject_identifier',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', unique=True, max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.subject_identifier_as_pk'
        db.add_column('bcpp_htc_htcregistration', 'subject_identifier_as_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.first_name'
        db.add_column('bcpp_htc_htcregistration', 'first_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.last_name'
        db.add_column('bcpp_htc_htcregistration', 'last_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.initials'
        db.add_column('bcpp_htc_htcregistration', 'initials',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.subject_type'
        db.add_column('bcpp_htc_htcregistration', 'subject_type',
                      self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.study_site'
        db.add_column('bcpp_htc_htcregistration', 'study_site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bhp_variables.StudySite']),
                      keep_default=False)

        # Adding field 'HtcRegistration.consent_datetime'
        db.add_column('bcpp_htc_htcregistration', 'consent_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'HtcRegistration.guardian_name'
        db.add_column('bcpp_htc_htcregistration', 'guardian_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.may_store_samples'
        db.add_column('bcpp_htc_htcregistration', 'may_store_samples',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistration.is_incarcerated'
        db.add_column('bcpp_htc_htcregistration', 'is_incarcerated',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistration.is_literate'
        db.add_column('bcpp_htc_htcregistration', 'is_literate',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistration.witness_name'
        db.add_column('bcpp_htc_htcregistration', 'witness_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.comment'
        db.add_column('bcpp_htc_htcregistration', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.consent_version_on_entry'
        db.add_column('bcpp_htc_htcregistration', 'consent_version_on_entry',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'HtcRegistration.consent_version_recent'
        db.add_column('bcpp_htc_htcregistration', 'consent_version_recent',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'HtcRegistration.consent_reviewed'
        db.add_column('bcpp_htc_htcregistration', 'consent_reviewed',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.study_questions'
        db.add_column('bcpp_htc_htcregistration', 'study_questions',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.assessment_score'
        db.add_column('bcpp_htc_htcregistration', 'assessment_score',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.consent_copy'
        db.add_column('bcpp_htc_htcregistration', 'consent_copy',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.language'
        db.add_column('bcpp_htc_htcregistration', 'language',
                      self.gf('django.db.models.fields.CharField')(default='not specified', max_length=25),
                      keep_default=False)

        # Adding field 'HtcRegistration.is_verified'
        db.add_column('bcpp_htc_htcregistration', 'is_verified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'HtcRegistration.is_verified_datetime'
        db.add_column('bcpp_htc_htcregistration', 'is_verified_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'HtcRegistration.identity'
        db.add_column('bcpp_htc_htcregistration', 'identity',
                      self.gf('django.db.models.fields.CharField')(default=0, unique=True, max_length=78L),
                      keep_default=False)

        # Adding field 'HtcRegistration.identity_type'
        db.add_column('bcpp_htc_htcregistration', 'identity_type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=15),
                      keep_default=False)

        # Adding field 'HtcRegistration.confirm_identity'
        db.add_column('bcpp_htc_htcregistration', 'confirm_identity',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.subject_identifier'
        db.add_column('bcpp_htc_htcregistration_audit', 'subject_identifier',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.subject_identifier_as_pk'
        db.add_column('bcpp_htc_htcregistration_audit', 'subject_identifier_as_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.first_name'
        db.add_column('bcpp_htc_htcregistration_audit', 'first_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.last_name'
        db.add_column('bcpp_htc_htcregistration_audit', 'last_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.initials'
        db.add_column('bcpp_htc_htcregistration_audit', 'initials',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.subject_type'
        db.add_column('bcpp_htc_htcregistration_audit', 'subject_type',
                      self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.study_site'
        db.add_column('bcpp_htc_htcregistration_audit', 'study_site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='_audit_htcregistration', to=orm['bhp_variables.StudySite']),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.consent_datetime'
        db.add_column('bcpp_htc_htcregistration_audit', 'consent_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.guardian_name'
        db.add_column('bcpp_htc_htcregistration_audit', 'guardian_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.may_store_samples'
        db.add_column('bcpp_htc_htcregistration_audit', 'may_store_samples',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.is_incarcerated'
        db.add_column('bcpp_htc_htcregistration_audit', 'is_incarcerated',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.is_literate'
        db.add_column('bcpp_htc_htcregistration_audit', 'is_literate',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=3),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.witness_name'
        db.add_column('bcpp_htc_htcregistration_audit', 'witness_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.comment'
        db.add_column('bcpp_htc_htcregistration_audit', 'comment',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.consent_version_on_entry'
        db.add_column('bcpp_htc_htcregistration_audit', 'consent_version_on_entry',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.consent_version_recent'
        db.add_column('bcpp_htc_htcregistration_audit', 'consent_version_recent',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.consent_reviewed'
        db.add_column('bcpp_htc_htcregistration_audit', 'consent_reviewed',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.study_questions'
        db.add_column('bcpp_htc_htcregistration_audit', 'study_questions',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.assessment_score'
        db.add_column('bcpp_htc_htcregistration_audit', 'assessment_score',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.consent_copy'
        db.add_column('bcpp_htc_htcregistration_audit', 'consent_copy',
                      self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.language'
        db.add_column('bcpp_htc_htcregistration_audit', 'language',
                      self.gf('django.db.models.fields.CharField')(default='not specified', max_length=25),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.is_verified'
        db.add_column('bcpp_htc_htcregistration_audit', 'is_verified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.is_verified_datetime'
        db.add_column('bcpp_htc_htcregistration_audit', 'is_verified_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.identity'
        db.add_column('bcpp_htc_htcregistration_audit', 'identity',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=78L),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.identity_type'
        db.add_column('bcpp_htc_htcregistration_audit', 'identity_type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=15),
                      keep_default=False)

        # Adding field 'HtcRegistrationAudit.confirm_identity'
        db.add_column('bcpp_htc_htcregistration_audit', 'confirm_identity',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'FollowupContactPermissionAudit'
        db.create_table('bcpp_htc_followupcontactpermission_audit', (
            ('pregnant_permission', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_followupcontactpermission', to=orm['bcpp_htc.HtcVisit'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('pregnant_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('male_contact', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('male_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_permission', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
        ))
        db.send_create_signal('bcpp_htc', ['FollowupContactPermissionAudit'])

        # Adding model 'ThirdPartner'
        db.create_table('bcpp_htc_thirdpartner', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('third_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['ThirdPartner'])

        # Adding model 'RecentPartnerAudit'
        db.create_table('bcpp_htc_recentpartner_audit', (
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_recentpartner', to=orm['bcpp_htc.HtcVisit'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('recent_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['RecentPartnerAudit'])

        # Adding model 'HivTestingCounselingAudit'
        db.create_table('bcpp_htc_hivtestingcounseling_audit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('clinic', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('cd4_result', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('partner_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cd4_test_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('reffered_to', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('symptoms', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('testing_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('couples_testing', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_hivtestingcounseling', to=orm['bcpp_htc.HtcVisit'])),
            ('circumcision_ap', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('reason_not_testing', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('family_tb', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('circumcision_ap_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('reffered_for', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('todays_result', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('bcpp_htc', ['HivTestingCounselingAudit'])

        # Adding model 'SecondPartner'
        db.create_table('bcpp_htc_secondpartner', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('second_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['SecondPartner'])

        # Adding model 'SecondPartnerAudit'
        db.create_table('bcpp_htc_secondpartner_audit', (
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('second_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_secondpartner', to=orm['bcpp_htc.HtcVisit'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['SecondPartnerAudit'])

        # Adding model 'ThirdPartnerAudit'
        db.create_table('bcpp_htc_thirdpartner_audit', (
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_thirdpartner', to=orm['bcpp_htc.HtcVisit'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('third_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['ThirdPartnerAudit'])

        # Adding model 'HivTestingCounseling'
        db.create_table('bcpp_htc_hivtestingcounseling', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('clinic', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('cd4_result', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('partner_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cd4_test_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('reffered_to', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('symptoms', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('testing_today', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('couples_testing', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('circumcision_ap', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('reason_not_testing', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('family_tb', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('circumcision_ap_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('reffered_for', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('todays_result', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('bcpp_htc', ['HivTestingCounseling'])

        # Adding model 'FollowupContactPermission'
        db.create_table('bcpp_htc_followupcontactpermission', (
            ('pregnant_permission', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('pregnant_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('male_contact', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('male_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('contact_permission', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('contact_family', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bcpp_htc', ['FollowupContactPermission'])

        # Adding model 'RecentPartner'
        db.create_table('bcpp_htc_recentpartner', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('htc_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bcpp_htc.HtcVisit'], unique=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('parter_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('recent_partner_rel', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 8, 21, 0, 0))),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('partner_tested', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('partner_residency', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bcpp_htc', ['RecentPartner'])

        # Deleting model 'Cd4Test'
        db.delete_table('bcpp_htc_cd4test')

        # Deleting model 'HtcSecondPartnerAudit'
        db.delete_table('bcpp_htc_htcsecondpartner_audit')

        # Deleting model 'HivTestingConsentAudit'
        db.delete_table('bcpp_htc_hivtestingconsent_audit')

        # Deleting model 'HtcRecentPartnerAudit'
        db.delete_table('bcpp_htc_htcrecentpartner_audit')

        # Deleting model 'CircumcisionAppointmentAudit'
        db.delete_table('bcpp_htc_circumcisionappointment_audit')

        # Deleting model 'PregnantFollowup'
        db.delete_table('bcpp_htc_pregnantfollowup')

        # Deleting model 'HtcSecondPartner'
        db.delete_table('bcpp_htc_htcsecondpartner')

        # Deleting model 'HivResult'
        db.delete_table('bcpp_htc_hivresult')

        # Deleting model 'Referral'
        db.delete_table('bcpp_htc_referral')

        # Removing M2M table for field referred_for on 'Referral'
        db.delete_table(db.shorten_name('bcpp_htc_referral_referred_for'))

        # Removing M2M table for field referred_to on 'Referral'
        db.delete_table(db.shorten_name('bcpp_htc_referral_referred_to'))

        # Deleting model 'HtcRecentPartner'
        db.delete_table('bcpp_htc_htcrecentpartner')

        # Deleting model 'HtcThirdPartnerAudit'
        db.delete_table('bcpp_htc_htcthirdpartner_audit')

        # Deleting model 'HivTestingConsent'
        db.delete_table('bcpp_htc_hivtestingconsent')

        # Deleting model 'Cd4TestAudit'
        db.delete_table('bcpp_htc_cd4test_audit')

        # Deleting model 'MaleFollowupAudit'
        db.delete_table('bcpp_htc_malefollowup_audit')

        # Deleting model 'HtcThirdPartner'
        db.delete_table('bcpp_htc_htcthirdpartner')

        # Deleting model 'PositiveFollowupAudit'
        db.delete_table('bcpp_htc_positivefollowup_audit')

        # Deleting model 'CircumcisionAppointment'
        db.delete_table('bcpp_htc_circumcisionappointment')

        # Deleting model 'PregnantFollowupAudit'
        db.delete_table('bcpp_htc_pregnantfollowup_audit')

        # Deleting model 'HivResultAudit'
        db.delete_table('bcpp_htc_hivresult_audit')

        # Deleting model 'MaleFollowup'
        db.delete_table('bcpp_htc_malefollowup')

        # Deleting model 'PositiveFollowup'
        db.delete_table('bcpp_htc_positivefollowup')

        # Deleting model 'ReferralAudit'
        db.delete_table('bcpp_htc_referral_audit')

        # Deleting field 'HtcRegistration.subject_identifier'
        db.delete_column('bcpp_htc_htcregistration', 'subject_identifier')

        # Deleting field 'HtcRegistration.subject_identifier_as_pk'
        db.delete_column('bcpp_htc_htcregistration', 'subject_identifier_as_pk')

        # Deleting field 'HtcRegistration.first_name'
        db.delete_column('bcpp_htc_htcregistration', 'first_name')

        # Deleting field 'HtcRegistration.last_name'
        db.delete_column('bcpp_htc_htcregistration', 'last_name')

        # Deleting field 'HtcRegistration.initials'
        db.delete_column('bcpp_htc_htcregistration', 'initials')

        # Deleting field 'HtcRegistration.subject_type'
        db.delete_column('bcpp_htc_htcregistration', 'subject_type')

        # Deleting field 'HtcRegistration.study_site'
        db.delete_column('bcpp_htc_htcregistration', 'study_site_id')

        # Deleting field 'HtcRegistration.consent_datetime'
        db.delete_column('bcpp_htc_htcregistration', 'consent_datetime')

        # Deleting field 'HtcRegistration.guardian_name'
        db.delete_column('bcpp_htc_htcregistration', 'guardian_name')

        # Deleting field 'HtcRegistration.may_store_samples'
        db.delete_column('bcpp_htc_htcregistration', 'may_store_samples')

        # Deleting field 'HtcRegistration.is_incarcerated'
        db.delete_column('bcpp_htc_htcregistration', 'is_incarcerated')

        # Deleting field 'HtcRegistration.is_literate'
        db.delete_column('bcpp_htc_htcregistration', 'is_literate')

        # Deleting field 'HtcRegistration.witness_name'
        db.delete_column('bcpp_htc_htcregistration', 'witness_name')

        # Deleting field 'HtcRegistration.comment'
        db.delete_column('bcpp_htc_htcregistration', 'comment')

        # Deleting field 'HtcRegistration.consent_version_on_entry'
        db.delete_column('bcpp_htc_htcregistration', 'consent_version_on_entry')

        # Deleting field 'HtcRegistration.consent_version_recent'
        db.delete_column('bcpp_htc_htcregistration', 'consent_version_recent')

        # Deleting field 'HtcRegistration.consent_reviewed'
        db.delete_column('bcpp_htc_htcregistration', 'consent_reviewed')

        # Deleting field 'HtcRegistration.study_questions'
        db.delete_column('bcpp_htc_htcregistration', 'study_questions')

        # Deleting field 'HtcRegistration.assessment_score'
        db.delete_column('bcpp_htc_htcregistration', 'assessment_score')

        # Deleting field 'HtcRegistration.consent_copy'
        db.delete_column('bcpp_htc_htcregistration', 'consent_copy')

        # Deleting field 'HtcRegistration.language'
        db.delete_column('bcpp_htc_htcregistration', 'language')

        # Deleting field 'HtcRegistration.is_verified'
        db.delete_column('bcpp_htc_htcregistration', 'is_verified')

        # Deleting field 'HtcRegistration.is_verified_datetime'
        db.delete_column('bcpp_htc_htcregistration', 'is_verified_datetime')

        # Deleting field 'HtcRegistration.identity'
        db.delete_column('bcpp_htc_htcregistration', 'identity')

        # Deleting field 'HtcRegistration.identity_type'
        db.delete_column('bcpp_htc_htcregistration', 'identity_type')

        # Deleting field 'HtcRegistration.confirm_identity'
        db.delete_column('bcpp_htc_htcregistration', 'confirm_identity')

        # Deleting field 'HtcRegistrationAudit.subject_identifier'
        db.delete_column('bcpp_htc_htcregistration_audit', 'subject_identifier')

        # Deleting field 'HtcRegistrationAudit.subject_identifier_as_pk'
        db.delete_column('bcpp_htc_htcregistration_audit', 'subject_identifier_as_pk')

        # Deleting field 'HtcRegistrationAudit.first_name'
        db.delete_column('bcpp_htc_htcregistration_audit', 'first_name')

        # Deleting field 'HtcRegistrationAudit.last_name'
        db.delete_column('bcpp_htc_htcregistration_audit', 'last_name')

        # Deleting field 'HtcRegistrationAudit.initials'
        db.delete_column('bcpp_htc_htcregistration_audit', 'initials')

        # Deleting field 'HtcRegistrationAudit.subject_type'
        db.delete_column('bcpp_htc_htcregistration_audit', 'subject_type')

        # Deleting field 'HtcRegistrationAudit.study_site'
        db.delete_column('bcpp_htc_htcregistration_audit', 'study_site_id')

        # Deleting field 'HtcRegistrationAudit.consent_datetime'
        db.delete_column('bcpp_htc_htcregistration_audit', 'consent_datetime')

        # Deleting field 'HtcRegistrationAudit.guardian_name'
        db.delete_column('bcpp_htc_htcregistration_audit', 'guardian_name')

        # Deleting field 'HtcRegistrationAudit.may_store_samples'
        db.delete_column('bcpp_htc_htcregistration_audit', 'may_store_samples')

        # Deleting field 'HtcRegistrationAudit.is_incarcerated'
        db.delete_column('bcpp_htc_htcregistration_audit', 'is_incarcerated')

        # Deleting field 'HtcRegistrationAudit.is_literate'
        db.delete_column('bcpp_htc_htcregistration_audit', 'is_literate')

        # Deleting field 'HtcRegistrationAudit.witness_name'
        db.delete_column('bcpp_htc_htcregistration_audit', 'witness_name')

        # Deleting field 'HtcRegistrationAudit.comment'
        db.delete_column('bcpp_htc_htcregistration_audit', 'comment')

        # Deleting field 'HtcRegistrationAudit.consent_version_on_entry'
        db.delete_column('bcpp_htc_htcregistration_audit', 'consent_version_on_entry')

        # Deleting field 'HtcRegistrationAudit.consent_version_recent'
        db.delete_column('bcpp_htc_htcregistration_audit', 'consent_version_recent')

        # Deleting field 'HtcRegistrationAudit.consent_reviewed'
        db.delete_column('bcpp_htc_htcregistration_audit', 'consent_reviewed')

        # Deleting field 'HtcRegistrationAudit.study_questions'
        db.delete_column('bcpp_htc_htcregistration_audit', 'study_questions')

        # Deleting field 'HtcRegistrationAudit.assessment_score'
        db.delete_column('bcpp_htc_htcregistration_audit', 'assessment_score')

        # Deleting field 'HtcRegistrationAudit.consent_copy'
        db.delete_column('bcpp_htc_htcregistration_audit', 'consent_copy')

        # Deleting field 'HtcRegistrationAudit.language'
        db.delete_column('bcpp_htc_htcregistration_audit', 'language')

        # Deleting field 'HtcRegistrationAudit.is_verified'
        db.delete_column('bcpp_htc_htcregistration_audit', 'is_verified')

        # Deleting field 'HtcRegistrationAudit.is_verified_datetime'
        db.delete_column('bcpp_htc_htcregistration_audit', 'is_verified_datetime')

        # Deleting field 'HtcRegistrationAudit.identity'
        db.delete_column('bcpp_htc_htcregistration_audit', 'identity')

        # Deleting field 'HtcRegistrationAudit.identity_type'
        db.delete_column('bcpp_htc_htcregistration_audit', 'identity_type')

        # Deleting field 'HtcRegistrationAudit.confirm_identity'
        db.delete_column('bcpp_htc_htcregistration_audit', 'confirm_identity')


    models = {
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'sub_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructure': {
            'Meta': {'unique_together': "(('household', 'survey'),)", 'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'Not Started'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.contactlog': {
            'Meta': {'object_name': 'ContactLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.householdmember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdMember'},
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.ContactLog']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']", 'null': 'True'}),
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
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.cd4test': {
            'Meta': {'object_name': 'Cd4Test'},
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'cd4_result': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_test_date': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'referral_clinic': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.cd4testaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'Cd4TestAudit', 'db_table': "'bcpp_htc_cd4test_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'cd4_result': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_test_date': ('django.db.models.fields.DateField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_cd4test'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'referral_clinic': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.circumcision': {
            'Meta': {'object_name': 'Circumcision'},
            'circumcision_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_circumcised': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.circumcisionappointment': {
            'Meta': {'object_name': 'CircumcisionAppointment'},
            'circumcision_ap': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_ap_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.circumcisionappointmentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisionAppointmentAudit', 'db_table': "'bcpp_htc_circumcisionappointment_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcision_ap': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_ap_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcisionappointment'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.circumcisionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisionAudit', 'db_table': "'bcpp_htc_circumcision_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcision_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcision'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_circumcised': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.demographicsrisk': {
            'Meta': {'object_name': 'DemographicsRisk'},
            'alcohol_intake': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'employment': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'marital_status': ('django.db.models.fields.IntegerField', [], {'max_length': '35'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.demographicsriskaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'DemographicsRiskAudit', 'db_table': "'bcpp_htc_demographicsrisk_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_intake': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'employment': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_demographicsrisk'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.IntegerField', [], {'max_length': '35'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivresult': {
            'Meta': {'object_name': 'HivResult'},
            'couples_testing': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'family_tb': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'symptoms': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'todays_result': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivresultaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivResultAudit', 'db_table': "'bcpp_htc_hivresult_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'couples_testing': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'family_tb': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivresult'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'partner_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'symptoms': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'todays_result': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivtestingconsent': {
            'Meta': {'object_name': 'HivTestingConsent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_not_testing': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'testing_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivtestingconsentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestingConsentAudit', 'db_table': "'bcpp_htc_hivtestingconsent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestingconsent'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_not_testing': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'testing_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivtestinghistory': {
            'Meta': {'object_name': 'HivTestingHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'previous_testing': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'result_obtained': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'testing_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.hivtestinghistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestingHistoryAudit', 'db_table': "'bcpp_htc_hivtestinghistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestinghistory'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'previous_testing': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'result_obtained': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'testing_place': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcrecentpartner': {
            'Meta': {'object_name': 'HtcRecentPartner'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'recent_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcrecentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HtcRecentPartnerAudit', 'db_table': "'bcpp_htc_htcrecentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcrecentpartner'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'recent_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcregistration': {
            'Meta': {'object_name': 'HtcRegistration'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_resident': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'omang': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'testing_counseling_site': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'your_community': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_htc.htcregistrationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HtcRegistrationAudit', 'db_table': "'bcpp_htc_htcregistration_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcregistration'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_resident': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'omang': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcregistration'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcregistration'", 'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'testing_counseling_site': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'your_community': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_htc.htcsecondpartner': {
            'Meta': {'object_name': 'HtcSecondPartner'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'second_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcsecondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HtcSecondPartnerAudit', 'db_table': "'bcpp_htc_htcsecondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcsecondpartner'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'second_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcthirdpartner': {
            'Meta': {'object_name': 'HtcThirdPartner'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'third_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcthirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HtcThirdPartnerAudit', 'db_table': "'bcpp_htc_htcthirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcthirdpartner'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parter_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'partner_tested': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'third_partner_rel': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.htcvisit': {
            'Meta': {'object_name': 'HtcVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.HouseholdMember']"}),
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
        'bcpp_htc.htcvisitaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HtcVisitAudit', 'db_table': "'bcpp_htc_htcvisit_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcvisit'", 'to': "orm['bhp_appointment.Appointment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_htcvisit'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
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
        'bcpp_htc.lasthivrecord': {
            'Meta': {'object_name': 'LastHivRecord'},
            'attended_hiv_care': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_care_card': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_care_clinic': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_result': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'recorded_test': ('django.db.models.fields.DateField', [], {}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.lasthivrecordaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LastHivRecordAudit', 'db_table': "'bcpp_htc_lasthivrecord_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'attended_hiv_care': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_care_card': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_care_clinic': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_lasthivrecord'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_result': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'recorded_test': ('django.db.models.fields.DateField', [], {}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.malefollowup': {
            'Meta': {'object_name': 'MaleFollowup'},
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.malefollowupaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MaleFollowupAudit', 'db_table': "'bcpp_htc_malefollowup_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_malefollowup'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.positivefollowup': {
            'Meta': {'object_name': 'PositiveFollowup'},
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.positivefollowupaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PositiveFollowupAudit', 'db_table': "'bcpp_htc_positivefollowup_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_positivefollowup'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.pregnantfollowup': {
            'Meta': {'object_name': 'PregnantFollowup'},
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.pregnantfollowupaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PregnantFollowupAudit', 'db_table': "'bcpp_htc_pregnantfollowup_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contact_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'contact_family': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_pregnantfollowup'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.referral': {
            'Meta': {'object_name': 'Referral'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_htc.HtcVisit']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'referred_for': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.ReferredFor']", 'symmetrical': 'False'}),
            'referred_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.ReferredTo']", 'symmetrical': 'False'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_htc.referralaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReferralAudit', 'db_table': "'bcpp_htc_referral_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'htc_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_referral'", 'to': "orm['bcpp_htc.HtcVisit']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 22, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_list.referredfor': {
            'Meta': {'object_name': 'ReferredFor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.referredto': {
            'Meta': {'object_name': 'ReferredTo'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_survey.survey': {
            'Meta': {'ordering': "['survey_name']", 'object_name': 'Survey'},
            'chronological_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple-2.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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

    complete_apps = ['bcpp_htc']
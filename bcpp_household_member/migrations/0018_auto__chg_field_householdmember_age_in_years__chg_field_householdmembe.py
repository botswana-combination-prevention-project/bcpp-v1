# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'HouseholdMember', fields ['registered_subject']
        db.delete_unique('bcpp_household_member_householdmember', ['registered_subject_id'])

        # Changing field 'HouseholdMember.age_in_years'
        db.alter_column('bcpp_household_member_householdmember', 'age_in_years', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'HouseholdMember.registered_subject'
        db.alter_column('bcpp_household_member_householdmember', 'registered_subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'], null=True))

        # Changing field 'HouseholdMember.nights_out'
        db.alter_column('bcpp_household_member_householdmember', 'nights_out', self.gf('django.db.models.fields.IntegerField')(null=True))


        # Changing field 'HouseholdMemberAudit.age_in_years'
        db.alter_column('bcpp_household_member_householdmember_audit', 'age_in_years', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'HouseholdMemberAudit.nights_out'
        db.alter_column('bcpp_household_member_householdmember_audit', 'nights_out', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Adding field 'HouseholdMemberAudit._audit_subject_identifier'
#         db.add_column('bcpp_household_member_householdmember_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

        # Adding field 'HouseholdInfoAudit._audit_subject_identifier'
#         db.add_column('bcpp_household_member_householdinfo_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)
#
#         # Adding field 'EnrolmentChecklistAudit._audit_subject_identifier'
#         db.add_column('bcpp_household_member_enrolmentchecklist_audit', '_audit_subject_identifier',
#                       self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
#                       keep_default=False)

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'HouseholdMember.age_in_years'
        raise RuntimeError("Cannot reverse this migration. 'HouseholdMember.age_in_years' and its values cannot be restored.")

        # Changing field 'HouseholdMember.registered_subject'
        db.alter_column('bcpp_household_member_householdmember', 'registered_subject_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_registration.RegisteredSubject'], unique=True, null=True))
        # Adding unique constraint on 'HouseholdMember', fields ['registered_subject']
        db.create_unique('bcpp_household_member_householdmember', ['registered_subject_id'])


        # User chose to not deal with backwards NULL issues for 'HouseholdMember.nights_out'
        raise RuntimeError("Cannot reverse this migration. 'HouseholdMember.nights_out' and its values cannot be restored.")
        # Deleting field 'HouseholdMemberAudit._audit_subject_identifier'
        db.delete_column('bcpp_household_member_householdmember_audit', '_audit_subject_identifier')


        # User chose to not deal with backwards NULL issues for 'HouseholdMemberAudit.age_in_years'
        raise RuntimeError("Cannot reverse this migration. 'HouseholdMemberAudit.age_in_years' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'HouseholdMemberAudit.nights_out'
        raise RuntimeError("Cannot reverse this migration. 'HouseholdMemberAudit.nights_out' and its values cannot be restored.")
        # Deleting field 'HouseholdInfoAudit._audit_subject_identifier'
        db.delete_column('bcpp_household_member_householdinfo_audit', '_audit_subject_identifier')

        # Deleting field 'EnrolmentChecklistAudit._audit_subject_identifier'
        db.delete_column('bcpp_household_member_enrolmentchecklist_audit', '_audit_subject_identifier')


    models = {
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
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
            'household_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'household_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_randomised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
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
            'member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
            'progress': ('django.db.models.fields.CharField', [], {'default': "'Not Started'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.plot': {
            'Meta': {'ordering': "['-plot_identifier']", 'unique_together': "(('gps_target_lat', 'gps_target_lon'),)", 'object_name': 'Plot'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'unconfirmed'", 'max_length': '25', 'null': 'True'}),
            'availability_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'eligible_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gps_degrees_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_degrees_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_minutes_e': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_minutes_s': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gps_target_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gps_target_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_household': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'plot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'sub_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'target_radius': ('django.db.models.fields.FloatField', [], {'default': '0.025'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.contactlog': {
            'Meta': {'object_name': 'ContactLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.contactlogitem': {
            'Meta': {'object_name': 'ContactLogItem'},
            'appointment_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contact_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'contact_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household_member.ContactLog']"}),
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
        'bcpp_household_member.enrolmentchecklist': {
            'Meta': {'object_name': 'EnrolmentChecklist'},
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'legal_marriage': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate_no': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'omang': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'reason_not_eligible': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.enrolmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'EnrolmentChecklistAudit', 'db_table': "'bcpp_household_member_enrolmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_enrolmentchecklist'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'legal_marriage': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'marriage_certificate_no': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'omang': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'reason_not_eligible': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_enrolmentchecklist'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.householdinfo': {
            'Meta': {'object_name': 'HouseholdInfo'},
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
            'household_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.HouseholdMember']", 'unique': 'True'}),
            'household_structure': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'transport_mode': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.TransportMode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_household_member.householdinfoaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdInfoAudit', 'db_table': "'bcpp_household_member_householdinfo_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
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
            'household_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdinfo'", 'to': "orm['bcpp_household_member.HouseholdMember']"}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdinfo'", 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdinfo'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_household_member.householdmember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdMember'},
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household_member.ContactLog']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']", 'null': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'is_eligible_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lives_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Plot']", 'null': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household_member.householdmemberaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdMemberAudit', 'db_table': "'bcpp_household_member_householdmember_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdmember'", 'null': 'True', 'to': "orm['bcpp_household_member.ContactLog']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdmember'", 'null': 'True', 'to': "orm['bcpp_household.Household']"}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_audit_householdmember'", 'null': 'True', 'to': "orm['bcpp_household.HouseholdStructure']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'is_eligible_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lives_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdmember'", 'null': 'True', 'to': "orm['bcpp_household.Plot']"}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdmember'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdmember'", 'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
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
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
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
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
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
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
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
        }
    }

    complete_apps = ['bcpp_household_member']
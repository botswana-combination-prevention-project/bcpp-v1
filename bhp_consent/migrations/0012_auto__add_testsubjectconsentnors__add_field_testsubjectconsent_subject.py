# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestSubjectConsentNoRS'
        db.create_table('bhp_consent_testsubjectconsentnors', (
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
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='No', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_consent', ['TestSubjectConsentNoRS'])

        # Adding field 'TestSubjectConsent.subject_identifier_as_pk'
        db.add_column('bhp_consent_testsubjectconsent', 'subject_identifier_as_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'TestSubjectConsent.is_literate'
        db.add_column('bhp_consent_testsubjectconsent', 'is_literate',
                      self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3),
                      keep_default=False)

        # Adding field 'TestSubjectConsent.witness_name'
        db.add_column('bhp_consent_testsubjectconsent', 'witness_name',
                      self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True),
                      keep_default=False)


        # Changing field 'TestSubjectConsent.subject_identifier'
        db.alter_column('bhp_consent_testsubjectconsent', 'subject_identifier', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50))
        # Adding unique constraint on 'TestSubjectConsent', fields ['subject_identifier']
        db.create_unique('bhp_consent_testsubjectconsent', ['subject_identifier'])


    def backwards(self, orm):
        # Removing unique constraint on 'TestSubjectConsent', fields ['subject_identifier']
        db.delete_unique('bhp_consent_testsubjectconsent', ['subject_identifier'])

        # Deleting model 'TestSubjectConsentNoRS'
        db.delete_table('bhp_consent_testsubjectconsentnors')

        # Deleting field 'TestSubjectConsent.subject_identifier_as_pk'
        db.delete_column('bhp_consent_testsubjectconsent', 'subject_identifier_as_pk')

        # Deleting field 'TestSubjectConsent.is_literate'
        db.delete_column('bhp_consent_testsubjectconsent', 'is_literate')

        # Deleting field 'TestSubjectConsent.witness_name'
        db.delete_column('bhp_consent_testsubjectconsent', 'witness_name')


        # Changing field 'TestSubjectConsent.subject_identifier'
        db.alter_column('bhp_consent_testsubjectconsent', 'subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))

    models = {
        'bhp_base_model.testforeignkey': {
            'Meta': {'object_name': 'TestForeignKey'},
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
        'bhp_base_model.testmanytomany': {
            'Meta': {'object_name': 'TestManyToMany'},
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
        'bhp_consent.attachedmodel': {
            'Meta': {'unique_together': "(('consent_catalogue', 'content_type_map'),)", 'object_name': 'AttachedModel'},
            'consent_catalogue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_consent.ConsentCatalogue']"}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_consent.attachedmodelaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'AttachedModelAudit', 'db_table': "'bhp_consent_attachedmodel_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'consent_catalogue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_attachedmodel'", 'to': "orm['bhp_consent.ConsentCatalogue']"}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_attachedmodel'", 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_consent.consentcatalogue': {
            'Meta': {'ordering': "['name', 'version']", 'unique_together': "(('name', 'version'),)", 'object_name': 'ConsentCatalogue'},
            'add_for_app': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'consent_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'list_for_update': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'bhp_consent.consentcatalogueaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ConsentCatalogueAudit', 'db_table': "'bhp_consent_consentcatalogue_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'add_for_app': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'consent_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_consentcatalogue'", 'null': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'list_for_update': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'bhp_consent.testsubjectconsent': {
            'Meta': {'object_name': 'TestSubjectConsent'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_provided_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bhp_consent.testsubjectconsentnors': {
            'Meta': {'object_name': 'TestSubjectConsentNoRS'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_provided_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bhp_consent.testsubjectuuidmodel': {
            'Meta': {'object_name': 'TestSubjectUuidModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'test_foreign_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_base_model.TestForeignKey']"}),
            'test_many_to_many': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_base_model.TestManyToMany']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
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
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('identity', 'first_name', 'dob', 'initials', 'registration_identifier'),)", 'object_name': 'RegisteredSubject'},
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bhp_consent']
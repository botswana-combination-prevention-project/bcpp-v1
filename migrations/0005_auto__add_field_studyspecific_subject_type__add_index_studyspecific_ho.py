# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StudySpecific.subject_type'
        db.add_column('bhp_variables_studyspecific', 'subject_type',
                      self.gf('django.db.models.fields.CharField')(default='subject', max_length=100),
                      keep_default=False)

        # Adding index on 'StudySpecific', fields ['hostname_created']
        db.create_index('bhp_variables_studyspecific', ['hostname_created'])

        # Adding index on 'StudySpecific', fields ['hostname_modified']
        db.create_index('bhp_variables_studyspecific', ['hostname_modified'])

        # Adding index on 'StudySpecific', fields ['user_created']
        db.create_index('bhp_variables_studyspecific', ['user_created'])

        # Adding index on 'StudySpecific', fields ['user_modified']
        db.create_index('bhp_variables_studyspecific', ['user_modified'])

        # Adding index on 'StudySite', fields ['hostname_created']
        db.create_index('bhp_variables_studysite', ['hostname_created'])

        # Adding unique constraint on 'StudySite', fields ['site_name']
        db.create_unique('bhp_variables_studysite', ['site_name'])

        # Adding unique constraint on 'StudySite', fields ['site_code']
        db.create_unique('bhp_variables_studysite', ['site_code'])

        # Adding index on 'StudySite', fields ['user_modified']
        db.create_index('bhp_variables_studysite', ['user_modified'])

        # Adding index on 'StudySite', fields ['hostname_modified']
        db.create_index('bhp_variables_studysite', ['hostname_modified'])

        # Adding index on 'StudySite', fields ['user_created']
        db.create_index('bhp_variables_studysite', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'StudySite', fields ['user_created']
        db.delete_index('bhp_variables_studysite', ['user_created'])

        # Removing index on 'StudySite', fields ['hostname_modified']
        db.delete_index('bhp_variables_studysite', ['hostname_modified'])

        # Removing index on 'StudySite', fields ['user_modified']
        db.delete_index('bhp_variables_studysite', ['user_modified'])

        # Removing unique constraint on 'StudySite', fields ['site_code']
        db.delete_unique('bhp_variables_studysite', ['site_code'])

        # Removing unique constraint on 'StudySite', fields ['site_name']
        db.delete_unique('bhp_variables_studysite', ['site_name'])

        # Removing index on 'StudySite', fields ['hostname_created']
        db.delete_index('bhp_variables_studysite', ['hostname_created'])

        # Removing index on 'StudySpecific', fields ['user_modified']
        db.delete_index('bhp_variables_studyspecific', ['user_modified'])

        # Removing index on 'StudySpecific', fields ['user_created']
        db.delete_index('bhp_variables_studyspecific', ['user_created'])

        # Removing index on 'StudySpecific', fields ['hostname_modified']
        db.delete_index('bhp_variables_studyspecific', ['hostname_modified'])

        # Removing index on 'StudySpecific', fields ['hostname_created']
        db.delete_index('bhp_variables_studyspecific', ['hostname_created'])

        # Deleting field 'StudySpecific.subject_type'
        db.delete_column('bhp_variables_studyspecific', 'subject_type')


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
        'bhp_variables.studyspecific': {
            'Meta': {'object_name': 'StudySpecific'},
            'age_at_adult_lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'gender_of_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_prefix': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'machine_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'maximum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'minimum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'protocol_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'protocol_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'protocol_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'research_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'study_start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier_modulus': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'subject_identifier_prefix': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'subject_identifier_seed': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '100'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_variables']
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StudySpecific'
        db.create_table('bhp_variables_studyspecific', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('protocol_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('protocol_title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('research_title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('study_start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('minimum_age_of_consent', self.gf('django.db.models.fields.IntegerField')()),
            ('maximum_age_of_consent', self.gf('django.db.models.fields.IntegerField')()),
            ('age_at_adult_lower_bound', self.gf('django.db.models.fields.IntegerField')(default=18)),
            ('gender_of_consent', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('subject_identifier_seed', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('subject_identifier_prefix', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('subject_identifier_modulus', self.gf('django.db.models.fields.IntegerField')(default=7)),
            ('hostname_prefix', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('bhp_variables', ['StudySpecific'])

        # Adding model 'StudySpecificSetting'
        db.create_table('bhp_variables_studyspecificsetting', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('setting_keyword', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('setting_value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('bhp_variables', ['StudySpecificSetting'])

        # Adding model 'StudySite'
        db.create_table('bhp_variables_studysite', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('site_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('bhp_variables', ['StudySite'])

        # Adding unique constraint on 'StudySite', fields ['site_code', 'site_name']
        db.create_unique('bhp_variables_studysite', ['site_code', 'site_name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'StudySite', fields ['site_code', 'site_name']
        db.delete_unique('bhp_variables_studysite', ['site_code', 'site_name'])

        # Deleting model 'StudySpecific'
        db.delete_table('bhp_variables_studyspecific')

        # Deleting model 'StudySpecificSetting'
        db.delete_table('bhp_variables_studyspecificsetting')

        # Deleting model 'StudySite'
        db.delete_table('bhp_variables_studysite')


    models = {
        'bhp_variables.studysite': {
            'Meta': {'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_variables.studyspecific': {
            'Meta': {'object_name': 'StudySpecific'},
            'age_at_adult_lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'gender_of_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_prefix': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'maximum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'minimum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'protocol_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'protocol_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'research_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'study_start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier_modulus': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'subject_identifier_prefix': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'subject_identifier_seed': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_variables.studyspecificsetting': {
            'Meta': {'ordering': "['setting_keyword']", 'object_name': 'StudySpecificSetting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'setting_keyword': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'setting_value': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_variables']

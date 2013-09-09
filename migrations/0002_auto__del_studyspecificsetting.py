# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'StudySpecificSetting'
        db.delete_table('bhp_variables_studyspecificsetting')


    def backwards(self, orm):
        
        # Adding model 'StudySpecificSetting'
        db.create_table('bhp_variables_studyspecificsetting', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('setting_value', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('setting_keyword', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_variables', ['StudySpecificSetting'])


    models = {
        'bhp_variables.studysite': {
            'Meta': {'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s014'", 'max_length': '50', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['bhp_variables']

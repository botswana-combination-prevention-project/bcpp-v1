# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("bhp_registration", "0001_initial"),
        ("bhp_visit", "0001_initial"),
    )


    def forwards(self, orm):
        
        # Adding model 'RegisteredSubjectAppointment'
        db.create_table('bhp_appointment_registeredsubjectappointment', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='dmc3', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('appt_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('dob', self.gf('django.db.models.fields.DateTimeField')()),
            ('appt_reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'])),
            ('visit_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_visit.VisitDefinition'])),
            ('visit_instance', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('bhp_appointment', ['RegisteredSubjectAppointment'])

        # Adding unique constraint on 'RegisteredSubjectAppointment', fields ['registered_subject', 'visit_definition', 'visit_instance']
        db.create_unique('bhp_appointment_registeredsubjectappointment', ['registered_subject_id', 'visit_definition_id', 'visit_instance'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'RegisteredSubjectAppointment', fields ['registered_subject', 'visit_definition', 'visit_instance']
        db.delete_unique('bhp_appointment_registeredsubjectappointment', ['registered_subject_id', 'visit_definition_id', 'visit_instance'])

        # Deleting model 'RegisteredSubjectAppointment'
        db.delete_table('bhp_appointment_registeredsubjectappointment')


    models = {
        'bhp_appointment.registeredsubjectappointment': {
            'Meta': {'unique_together': "[('registered_subject', 'visit_definition', 'visit_instance')]", 'object_name': 'RegisteredSubjectAppointment'},
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_visit.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.IntegerField', [], {})
        },
        'bhp_registration.registeredsubject': {
            'Meta': {'object_name': 'RegisteredSubject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_visit.visitdefinition': {
            'Meta': {'ordering': "['time_point']", 'object_name': 'VisitDefinition'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'dmc3'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {}),
            'time_point_unit': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'time_point_window_period_post': ('django.db.models.fields.IntegerField', [], {}),
            'time_point_window_period_pre': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_appointment']

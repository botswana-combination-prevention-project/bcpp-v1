# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TagForSchedule'
        db.create_table('bhp_visit_tagforschedule', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('entry_form', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttypes.ContentType'], unique=True)),
            ('tag_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('grouping_key', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_visit', ['TagForSchedule'])

        # Adding model 'VisitDefinition'
        db.create_table('bhp_visit_visitdefinition', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('time_point', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lower_window', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lower_window_unit', self.gf('django.db.models.fields.CharField')(default='D', max_length=10)),
            ('upper_window', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('upper_window_unit', self.gf('django.db.models.fields.CharField')(default='D', max_length=10)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('instruction', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('bhp_visit', ['VisitDefinition'])

        # Adding M2M table for field tag_for_schedule on 'VisitDefinition'
        db.create_table('bhp_visit_visitdefinition_tag_for_schedule', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visitdefinition', models.ForeignKey(orm['bhp_visit.visitdefinition'], null=False)),
            ('tagforschedule', models.ForeignKey(orm['bhp_visit.tagforschedule'], null=False))
        ))
        db.create_unique('bhp_visit_visitdefinition_tag_for_schedule', ['visitdefinition_id', 'tagforschedule_id'])

        # Adding model 'Appointment'
        db.create_table('bhp_visit_appointment', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('appt_status', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('appt_reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_registration.RegisteredSubject'])),
            ('visit_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_visit.VisitDefinition'])),
            ('visit_instance', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('bhp_visit', ['Appointment'])

        # Adding unique constraint on 'Appointment', fields ['registered_subject', 'visit_definition', 'visit_instance']
        db.create_unique('bhp_visit_appointment', ['registered_subject_id', 'visit_definition_id', 'visit_instance'])

        # Adding model 'VisitTrackingInfoSource'
        db.create_table('bhp_visit_visittrackinginfosource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('bhp_visit', ['VisitTrackingInfoSource'])

        # Adding model 'VisitTrackingVisitReason'
        db.create_table('bhp_visit_visittrackingvisitreason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_visit', ['VisitTrackingVisitReason'])

        # Adding model 'VisitTrackingSubjCurrStatus'
        db.create_table('bhp_visit_visittrackingsubjcurrstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('bhp_visit', ['VisitTrackingSubjCurrStatus'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Appointment', fields ['registered_subject', 'visit_definition', 'visit_instance']
        db.delete_unique('bhp_visit_appointment', ['registered_subject_id', 'visit_definition_id', 'visit_instance'])

        # Deleting model 'TagForSchedule'
        db.delete_table('bhp_visit_tagforschedule')

        # Deleting model 'VisitDefinition'
        db.delete_table('bhp_visit_visitdefinition')

        # Removing M2M table for field tag_for_schedule on 'VisitDefinition'
        db.delete_table('bhp_visit_visitdefinition_tag_for_schedule')

        # Deleting model 'Appointment'
        db.delete_table('bhp_visit_appointment')

        # Deleting model 'VisitTrackingInfoSource'
        db.delete_table('bhp_visit_visittrackinginfosource')

        # Deleting model 'VisitTrackingVisitReason'
        db.delete_table('bhp_visit_visittrackingvisitreason')

        # Deleting model 'VisitTrackingSubjCurrStatus'
        db.delete_table('bhp_visit_visittrackingsubjcurrstatus')


    models = {
        'bhp_registration.registeredsubject': {
            'Meta': {'object_name': 'RegisteredSubject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
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
        'bhp_visit.appointment': {
            'Meta': {'ordering': "['registered_subject', 'appt_datetime']", 'unique_together': "[('registered_subject', 'visit_definition', 'visit_instance')]", 'object_name': 'Appointment'},
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_visit.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'bhp_visit.tagforschedule': {
            'Meta': {'object_name': 'TagForSchedule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entry_form': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttypes.ContentType']", 'unique': 'True'}),
            'grouping_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'tag_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_visit.visitdefinition': {
            'Meta': {'ordering': "['time_point']", 'object_name': 'VisitDefinition'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'lower_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lower_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'tag_for_schedule': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_visit.TagForSchedule']", 'symmetrical': 'False'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'upper_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upper_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_visit.visittrackinginfosource': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'VisitTrackingInfoSource'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_visit.visittrackingsubjcurrstatus': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'VisitTrackingSubjCurrStatus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_visit.visittrackingvisitreason': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'VisitTrackingVisitReason'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bhp_visit']

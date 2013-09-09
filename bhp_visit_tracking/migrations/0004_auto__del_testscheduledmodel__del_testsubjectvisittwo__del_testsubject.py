# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestScheduledModel'
        db.delete_table('bhp_visit_tracking_testscheduledmodel')

        # Deleting model 'TestSubjectVisitTwo'
        db.delete_table('bhp_visit_tracking_testsubjectvisittwo')

        # Deleting model 'TestSubjectVisit'
        db.delete_table('bhp_visit_tracking_testsubjectvisit')

        # Deleting model 'TestSubjectVisitThree'
        db.delete_table('bhp_visit_tracking_testsubjectvisitthree')


    def backwards(self, orm):
        # Adding model 'TestScheduledModel'
        db.create_table('bhp_visit_tracking_testscheduledmodel', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('test_subject_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_visit_tracking.TestSubjectVisit'], unique=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_visit_tracking', ['TestScheduledModel'])

        # Adding model 'TestSubjectVisitTwo'
        db.create_table('bhp_visit_tracking_testsubjectvisittwo', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_appointment.Appointment'], unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_visit_tracking', ['TestSubjectVisitTwo'])

        # Adding model 'TestSubjectVisit'
        db.create_table('bhp_visit_tracking_testsubjectvisit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_appointment.Appointment'], unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_visit_tracking', ['TestSubjectVisit'])

        # Adding model 'TestSubjectVisitThree'
        db.create_table('bhp_visit_tracking_testsubjectvisitthree', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bhp_appointment.Appointment'], unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='honeypot', max_length=50, blank=True, db_index=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('bhp_visit_tracking', ['TestSubjectVisitThree'])


    models = {
        
    }

    complete_apps = ['bhp_visit_tracking']
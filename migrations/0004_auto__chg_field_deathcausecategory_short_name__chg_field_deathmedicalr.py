# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'DeathCauseCategory', fields ['name']
        db.create_index('bhp_adverse_deathcausecategory', ['name'])


        # Changing field 'DeathCauseCategory.short_name'
        db.alter_column('bhp_adverse_deathcausecategory', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'DeathCauseCategory', fields ['short_name']
        db.create_index('bhp_adverse_deathcausecategory', ['short_name'])

        # Adding index on 'DeathCauseCategory', fields ['user_modified']
        db.create_index('bhp_adverse_deathcausecategory', ['user_modified'])

        # Adding index on 'DeathCauseCategory', fields ['display_index']
        db.create_index('bhp_adverse_deathcausecategory', ['display_index'])

        # Adding index on 'DeathCauseCategory', fields ['user_created']
        db.create_index('bhp_adverse_deathcausecategory', ['user_created'])

        # Adding index on 'SimpleAdverseEvent', fields ['user_modified']
        db.create_index('bhp_adverse_simpleadverseevent', ['user_modified'])

        # Adding index on 'SimpleAdverseEvent', fields ['user_created']
        db.create_index('bhp_adverse_simpleadverseevent', ['user_created'])

        # Adding index on 'DeathMedicalResponsibility', fields ['name']
        db.create_index('bhp_adverse_deathmedicalresponsibility', ['name'])


        # Changing field 'DeathMedicalResponsibility.short_name'
        db.alter_column('bhp_adverse_deathmedicalresponsibility', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'DeathMedicalResponsibility', fields ['short_name']
        db.create_index('bhp_adverse_deathmedicalresponsibility', ['short_name'])

        # Adding index on 'DeathMedicalResponsibility', fields ['user_modified']
        db.create_index('bhp_adverse_deathmedicalresponsibility', ['user_modified'])

        # Adding index on 'DeathMedicalResponsibility', fields ['display_index']
        db.create_index('bhp_adverse_deathmedicalresponsibility', ['display_index'])

        # Adding index on 'DeathMedicalResponsibility', fields ['user_created']
        db.create_index('bhp_adverse_deathmedicalresponsibility', ['user_created'])

        # Adding index on 'Ae010ReportType', fields ['name']
        db.create_index('bhp_adverse_ae010reporttype', ['name'])


        # Changing field 'Ae010ReportType.short_name'
        db.alter_column('bhp_adverse_ae010reporttype', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'Ae010ReportType', fields ['short_name']
        db.create_index('bhp_adverse_ae010reporttype', ['short_name'])

        # Adding index on 'Ae010ReportType', fields ['user_modified']
        db.create_index('bhp_adverse_ae010reporttype', ['user_modified'])

        # Adding index on 'Ae010ReportType', fields ['display_index']
        db.create_index('bhp_adverse_ae010reporttype', ['display_index'])

        # Adding index on 'Ae010ReportType', fields ['user_created']
        db.create_index('bhp_adverse_ae010reporttype', ['user_created'])

        # Adding index on 'DeathCauseInfo', fields ['name']
        db.create_index('bhp_adverse_deathcauseinfo', ['name'])


        # Changing field 'DeathCauseInfo.short_name'
        db.alter_column('bhp_adverse_deathcauseinfo', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'DeathCauseInfo', fields ['short_name']
        db.create_index('bhp_adverse_deathcauseinfo', ['short_name'])

        # Adding index on 'DeathCauseInfo', fields ['user_modified']
        db.create_index('bhp_adverse_deathcauseinfo', ['user_modified'])

        # Adding index on 'DeathCauseInfo', fields ['display_index']
        db.create_index('bhp_adverse_deathcauseinfo', ['display_index'])

        # Adding index on 'DeathCauseInfo', fields ['user_created']
        db.create_index('bhp_adverse_deathcauseinfo', ['user_created'])

        # Adding index on 'Ae010AdverseStudyRel', fields ['name']
        db.create_index('bhp_adverse_ae010adversestudyrel', ['name'])


        # Changing field 'Ae010AdverseStudyRel.short_name'
        db.alter_column('bhp_adverse_ae010adversestudyrel', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'Ae010AdverseStudyRel', fields ['short_name']
        db.create_index('bhp_adverse_ae010adversestudyrel', ['short_name'])

        # Adding index on 'Ae010AdverseStudyRel', fields ['user_modified']
        db.create_index('bhp_adverse_ae010adversestudyrel', ['user_modified'])

        # Adding index on 'Ae010AdverseStudyRel', fields ['display_index']
        db.create_index('bhp_adverse_ae010adversestudyrel', ['display_index'])

        # Adding index on 'Ae010AdverseStudyRel', fields ['user_created']
        db.create_index('bhp_adverse_ae010adversestudyrel', ['user_created'])

        # Adding index on 'DeathReasonHospitalized', fields ['name']
        db.create_index('bhp_adverse_deathreasonhospitalized', ['name'])


        # Changing field 'DeathReasonHospitalized.short_name'
        db.alter_column('bhp_adverse_deathreasonhospitalized', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'DeathReasonHospitalized', fields ['short_name']
        db.create_index('bhp_adverse_deathreasonhospitalized', ['short_name'])

        # Adding index on 'DeathReasonHospitalized', fields ['user_modified']
        db.create_index('bhp_adverse_deathreasonhospitalized', ['user_modified'])

        # Adding index on 'DeathReasonHospitalized', fields ['display_index']
        db.create_index('bhp_adverse_deathreasonhospitalized', ['display_index'])

        # Adding index on 'DeathReasonHospitalized', fields ['user_created']
        db.create_index('bhp_adverse_deathreasonhospitalized', ['user_created'])

        # Adding index on 'AdverseEventReportType', fields ['name']
        db.create_index('bhp_adverse_adverseeventreporttype', ['name'])


        # Changing field 'AdverseEventReportType.short_name'
        db.alter_column('bhp_adverse_adverseeventreporttype', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'AdverseEventReportType', fields ['short_name']
        db.create_index('bhp_adverse_adverseeventreporttype', ['short_name'])

        # Adding index on 'AdverseEventReportType', fields ['user_modified']
        db.create_index('bhp_adverse_adverseeventreporttype', ['user_modified'])

        # Adding index on 'AdverseEventReportType', fields ['display_index']
        db.create_index('bhp_adverse_adverseeventreporttype', ['display_index'])

        # Adding index on 'AdverseEventReportType', fields ['user_created']
        db.create_index('bhp_adverse_adverseeventreporttype', ['user_created'])

        # Adding index on 'AdverseEventStudyRelation', fields ['name']
        db.create_index('bhp_adverse_adverseeventstudyrelation', ['name'])


        # Changing field 'AdverseEventStudyRelation.short_name'
        db.alter_column('bhp_adverse_adverseeventstudyrelation', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True))
        # Adding index on 'AdverseEventStudyRelation', fields ['short_name']
        db.create_index('bhp_adverse_adverseeventstudyrelation', ['short_name'])

        # Adding index on 'AdverseEventStudyRelation', fields ['user_modified']
        db.create_index('bhp_adverse_adverseeventstudyrelation', ['user_modified'])

        # Adding index on 'AdverseEventStudyRelation', fields ['display_index']
        db.create_index('bhp_adverse_adverseeventstudyrelation', ['display_index'])

        # Adding index on 'AdverseEventStudyRelation', fields ['user_created']
        db.create_index('bhp_adverse_adverseeventstudyrelation', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'AdverseEventStudyRelation', fields ['user_created']
        db.delete_index('bhp_adverse_adverseeventstudyrelation', ['user_created'])

        # Removing index on 'AdverseEventStudyRelation', fields ['display_index']
        db.delete_index('bhp_adverse_adverseeventstudyrelation', ['display_index'])

        # Removing index on 'AdverseEventStudyRelation', fields ['user_modified']
        db.delete_index('bhp_adverse_adverseeventstudyrelation', ['user_modified'])

        # Removing index on 'AdverseEventStudyRelation', fields ['short_name']
        db.delete_index('bhp_adverse_adverseeventstudyrelation', ['short_name'])

        # Removing index on 'AdverseEventStudyRelation', fields ['name']
        db.delete_index('bhp_adverse_adverseeventstudyrelation', ['name'])

        # Removing index on 'AdverseEventReportType', fields ['user_created']
        db.delete_index('bhp_adverse_adverseeventreporttype', ['user_created'])

        # Removing index on 'AdverseEventReportType', fields ['display_index']
        db.delete_index('bhp_adverse_adverseeventreporttype', ['display_index'])

        # Removing index on 'AdverseEventReportType', fields ['user_modified']
        db.delete_index('bhp_adverse_adverseeventreporttype', ['user_modified'])

        # Removing index on 'AdverseEventReportType', fields ['short_name']
        db.delete_index('bhp_adverse_adverseeventreporttype', ['short_name'])

        # Removing index on 'AdverseEventReportType', fields ['name']
        db.delete_index('bhp_adverse_adverseeventreporttype', ['name'])

        # Removing index on 'DeathReasonHospitalized', fields ['user_created']
        db.delete_index('bhp_adverse_deathreasonhospitalized', ['user_created'])

        # Removing index on 'DeathReasonHospitalized', fields ['display_index']
        db.delete_index('bhp_adverse_deathreasonhospitalized', ['display_index'])

        # Removing index on 'DeathReasonHospitalized', fields ['user_modified']
        db.delete_index('bhp_adverse_deathreasonhospitalized', ['user_modified'])

        # Removing index on 'DeathReasonHospitalized', fields ['short_name']
        db.delete_index('bhp_adverse_deathreasonhospitalized', ['short_name'])

        # Removing index on 'DeathReasonHospitalized', fields ['name']
        db.delete_index('bhp_adverse_deathreasonhospitalized', ['name'])

        # Removing index on 'Ae010AdverseStudyRel', fields ['user_created']
        db.delete_index('bhp_adverse_ae010adversestudyrel', ['user_created'])

        # Removing index on 'Ae010AdverseStudyRel', fields ['display_index']
        db.delete_index('bhp_adverse_ae010adversestudyrel', ['display_index'])

        # Removing index on 'Ae010AdverseStudyRel', fields ['user_modified']
        db.delete_index('bhp_adverse_ae010adversestudyrel', ['user_modified'])

        # Removing index on 'Ae010AdverseStudyRel', fields ['short_name']
        db.delete_index('bhp_adverse_ae010adversestudyrel', ['short_name'])

        # Removing index on 'Ae010AdverseStudyRel', fields ['name']
        db.delete_index('bhp_adverse_ae010adversestudyrel', ['name'])

        # Removing index on 'DeathCauseInfo', fields ['user_created']
        db.delete_index('bhp_adverse_deathcauseinfo', ['user_created'])

        # Removing index on 'DeathCauseInfo', fields ['display_index']
        db.delete_index('bhp_adverse_deathcauseinfo', ['display_index'])

        # Removing index on 'DeathCauseInfo', fields ['user_modified']
        db.delete_index('bhp_adverse_deathcauseinfo', ['user_modified'])

        # Removing index on 'DeathCauseInfo', fields ['short_name']
        db.delete_index('bhp_adverse_deathcauseinfo', ['short_name'])

        # Removing index on 'DeathCauseInfo', fields ['name']
        db.delete_index('bhp_adverse_deathcauseinfo', ['name'])

        # Removing index on 'Ae010ReportType', fields ['user_created']
        db.delete_index('bhp_adverse_ae010reporttype', ['user_created'])

        # Removing index on 'Ae010ReportType', fields ['display_index']
        db.delete_index('bhp_adverse_ae010reporttype', ['display_index'])

        # Removing index on 'Ae010ReportType', fields ['user_modified']
        db.delete_index('bhp_adverse_ae010reporttype', ['user_modified'])

        # Removing index on 'Ae010ReportType', fields ['short_name']
        db.delete_index('bhp_adverse_ae010reporttype', ['short_name'])

        # Removing index on 'Ae010ReportType', fields ['name']
        db.delete_index('bhp_adverse_ae010reporttype', ['name'])

        # Removing index on 'DeathMedicalResponsibility', fields ['user_created']
        db.delete_index('bhp_adverse_deathmedicalresponsibility', ['user_created'])

        # Removing index on 'DeathMedicalResponsibility', fields ['display_index']
        db.delete_index('bhp_adverse_deathmedicalresponsibility', ['display_index'])

        # Removing index on 'DeathMedicalResponsibility', fields ['user_modified']
        db.delete_index('bhp_adverse_deathmedicalresponsibility', ['user_modified'])

        # Removing index on 'DeathMedicalResponsibility', fields ['short_name']
        db.delete_index('bhp_adverse_deathmedicalresponsibility', ['short_name'])

        # Removing index on 'DeathMedicalResponsibility', fields ['name']
        db.delete_index('bhp_adverse_deathmedicalresponsibility', ['name'])

        # Removing index on 'SimpleAdverseEvent', fields ['user_created']
        db.delete_index('bhp_adverse_simpleadverseevent', ['user_created'])

        # Removing index on 'SimpleAdverseEvent', fields ['user_modified']
        db.delete_index('bhp_adverse_simpleadverseevent', ['user_modified'])

        # Removing index on 'DeathCauseCategory', fields ['user_created']
        db.delete_index('bhp_adverse_deathcausecategory', ['user_created'])

        # Removing index on 'DeathCauseCategory', fields ['display_index']
        db.delete_index('bhp_adverse_deathcausecategory', ['display_index'])

        # Removing index on 'DeathCauseCategory', fields ['user_modified']
        db.delete_index('bhp_adverse_deathcausecategory', ['user_modified'])

        # Removing index on 'DeathCauseCategory', fields ['short_name']
        db.delete_index('bhp_adverse_deathcausecategory', ['short_name'])

        # Removing index on 'DeathCauseCategory', fields ['name']
        db.delete_index('bhp_adverse_deathcausecategory', ['name'])


        # Changing field 'DeathCauseCategory.short_name'
        db.alter_column('bhp_adverse_deathcausecategory', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'DeathMedicalResponsibility.short_name'
        db.alter_column('bhp_adverse_deathmedicalresponsibility', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'Ae010ReportType.short_name'
        db.alter_column('bhp_adverse_ae010reporttype', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'DeathCauseInfo.short_name'
        db.alter_column('bhp_adverse_deathcauseinfo', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'Ae010AdverseStudyRel.short_name'
        db.alter_column('bhp_adverse_ae010adversestudyrel', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'DeathReasonHospitalized.short_name'
        db.alter_column('bhp_adverse_deathreasonhospitalized', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'AdverseEventReportType.short_name'
        db.alter_column('bhp_adverse_adverseeventreporttype', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

        # Changing field 'AdverseEventStudyRelation.short_name'
        db.alter_column('bhp_adverse_adverseeventstudyrelation', 'short_name', self.gf('django.db.models.fields.CharField')(default='-', max_length=250, unique=True))

    models = {
        'bhp_adverse.adverseeventreporttype': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'AdverseEventReportType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_adverse.adverseeventstudyrelation': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'AdverseEventStudyRelation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_adverse.ae010adversestudyrel': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'Ae010AdverseStudyRel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_adverse.ae010reporttype': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'Ae010ReportType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_adverse.deathmedicalresponsibility': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathMedicalResponsibility'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_adverse.simpleadverseevent': {
            'Meta': {'object_name': 'SimpleAdverseEvent'},
            'adverse_study_rel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.Ae010AdverseStudyRel']"}),
            'ae_desc': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_onset': ('django.db.models.fields.DateField', [], {}),
            'event_grade': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.Ae010ReportType']"}),
            'study_coord': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
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
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'null': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['bhp_adverse']
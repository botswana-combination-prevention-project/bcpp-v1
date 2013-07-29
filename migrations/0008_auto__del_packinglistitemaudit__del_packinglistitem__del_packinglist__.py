# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        #raise TypeError('WAIT! lab_packing 0008 deletes the lab_packing table. Back it up and remove this raise error.')
        # Deleting model 'PackingListItemAudit'
        db.delete_table('lab_packing_packinglistitem_audit')

        # Deleting model 'PackingListItem'
        db.delete_table('lab_packing_packinglistitem')

        # Deleting model 'PackingList'
        db.delete_table('lab_packing_packinglist')

        # Deleting model 'PackingListAudit'
        db.delete_table('lab_packing_packinglist_audit')


    def backwards(self, orm):
        
        # Adding model 'PackingListItemAudit'
        db.create_table('lab_packing_packinglistitem_audit', (
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('item_reference', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('packing_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_packinglistitem', to=orm['lab_packing.PackingList'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('item_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('item_description', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_packinglistitem', null=True, to=orm['lab_panel.Panel'], blank=True)),
        ))
        db.send_create_signal('lab_packing', ['PackingListItemAudit'])

        # Adding model 'PackingListItem'
        db.create_table('lab_packing_packinglistitem', (
            ('item_reference', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('packing_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_packing.PackingList'])),
            ('item_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('item_description', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_panel.Panel'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('lab_packing', ['PackingListItem'])

        # Adding model 'PackingList'
        db.create_table('lab_packing_packinglist', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('list_comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('list_items', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('list_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 2, 10, 22, 25, 45896))),
        ))
        db.send_create_signal('lab_packing', ['PackingList'])

        # Adding model 'PackingListAudit'
        db.create_table('lab_packing_packinglist_audit', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('list_comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('list_items', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('list_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 4, 2, 10, 22, 25, 45896))),
        ))
        db.send_create_signal('lab_packing', ['PackingListAudit'])


    models = {
        
    }

    complete_apps = ['lab_packing']

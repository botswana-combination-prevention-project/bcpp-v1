# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AccountHolder'
        db.create_table('bhp_lab_registration_accountholder', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='s007', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='s007', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('lab_account', ['AccountHolder'])

        # Adding unique constraint on 'AccountHolder', fields ['last_name', 'first_name']
        db.create_unique('bhp_lab_registration_accountholder', ['last_name', 'first_name'])

        # Adding model 'Account'
        db.create_table('bhp_lab_registration_account', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='s007', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='s007', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('account_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('account_opendate', self.gf('django.db.models.fields.DateField')()),
            ('account_closedate', self.gf('django.db.models.fields.DateField')()),
            ('account_holder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_account.AccountHolder'], null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('lab_account', ['Account'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AccountHolder', fields ['last_name', 'first_name']
        db.delete_unique('bhp_lab_registration_accountholder', ['last_name', 'first_name'])

        # Deleting model 'AccountHolder'
        db.delete_table('bhp_lab_registration_accountholder')

        # Deleting model 'Account'
        db.delete_table('bhp_lab_registration_account')


    models = {
        'lab_account.account': {
            'Meta': {'ordering': "['account_name']", 'object_name': 'Account', 'db_table': "'bhp_lab_registration_account'"},
            'account_closedate': ('django.db.models.fields.DateField', [], {}),
            'account_holder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_account.AccountHolder']", 'null': 'True'}),
            'account_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'account_opendate': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'lab_account.accountholder': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'AccountHolder', 'db_table': "'bhp_lab_registration_accountholder'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['lab_account']

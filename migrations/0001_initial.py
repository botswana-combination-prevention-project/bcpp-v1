# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FundingSource'
        db.create_table('bhp_research_protocol_fundingsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('bhp_research_protocol', ['FundingSource'])

        # Adding model 'PrincipalInvestigator'
        db.create_table('bhp_research_protocol_principalinvestigator', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bhp_research_protocol', ['PrincipalInvestigator'])

        # Adding unique constraint on 'PrincipalInvestigator', fields ['last_name', 'first_name']
        db.create_unique('bhp_research_protocol_principalinvestigator', ['last_name', 'first_name'])

        # Adding model 'SiteLeader'
        db.create_table('bhp_research_protocol_siteleader', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='home', max_length=50, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('bhp_research_protocol', ['SiteLeader'])

        # Adding unique constraint on 'SiteLeader', fields ['last_name', 'first_name']
        db.create_unique('bhp_research_protocol_siteleader', ['last_name', 'first_name'])

        # Adding model 'Protocol'
        db.create_table('bhp_research_protocol_protocol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('protocol_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('research_title', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('local_title', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('date_registered', self.gf('django.db.models.fields.DateField')()),
            ('date_opened', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('bhp_research_protocol', ['Protocol'])

        # Adding M2M table for field prinicipal_investigator on 'Protocol'
        db.create_table('bhp_research_protocol_protocol_prinicipal_investigator', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('protocol', models.ForeignKey(orm['bhp_research_protocol.protocol'], null=False)),
            ('principalinvestigator', models.ForeignKey(orm['bhp_research_protocol.principalinvestigator'], null=False))
        ))
        db.create_unique('bhp_research_protocol_protocol_prinicipal_investigator', ['protocol_id', 'principalinvestigator_id'])

        # Adding M2M table for field site_leader on 'Protocol'
        db.create_table('bhp_research_protocol_protocol_site_leader', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('protocol', models.ForeignKey(orm['bhp_research_protocol.protocol'], null=False)),
            ('siteleader', models.ForeignKey(orm['bhp_research_protocol.siteleader'], null=False))
        ))
        db.create_unique('bhp_research_protocol_protocol_site_leader', ['protocol_id', 'siteleader_id'])

        # Adding M2M table for field funding_source on 'Protocol'
        db.create_table('bhp_research_protocol_protocol_funding_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('protocol', models.ForeignKey(orm['bhp_research_protocol.protocol'], null=False)),
            ('fundingsource', models.ForeignKey(orm['bhp_research_protocol.fundingsource'], null=False))
        ))
        db.create_unique('bhp_research_protocol_protocol_funding_source', ['protocol_id', 'fundingsource_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SiteLeader', fields ['last_name', 'first_name']
        db.delete_unique('bhp_research_protocol_siteleader', ['last_name', 'first_name'])

        # Removing unique constraint on 'PrincipalInvestigator', fields ['last_name', 'first_name']
        db.delete_unique('bhp_research_protocol_principalinvestigator', ['last_name', 'first_name'])

        # Deleting model 'FundingSource'
        db.delete_table('bhp_research_protocol_fundingsource')

        # Deleting model 'PrincipalInvestigator'
        db.delete_table('bhp_research_protocol_principalinvestigator')

        # Deleting model 'SiteLeader'
        db.delete_table('bhp_research_protocol_siteleader')

        # Deleting model 'Protocol'
        db.delete_table('bhp_research_protocol_protocol')

        # Removing M2M table for field prinicipal_investigator on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_prinicipal_investigator')

        # Removing M2M table for field site_leader on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_site_leader')

        # Removing M2M table for field funding_source on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_funding_source')


    models = {
        'bhp_research_protocol.fundingsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'FundingSource'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'bhp_research_protocol.principalinvestigator': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'PrincipalInvestigator'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_research_protocol.protocol': {
            'Meta': {'ordering': "['protocol_identifier']", 'object_name': 'Protocol'},
            'date_opened': ('django.db.models.fields.DateField', [], {}),
            'date_registered': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'funding_source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.FundingSource']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_title': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'prinicipal_investigator': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.PrincipalInvestigator']", 'symmetrical': 'False'}),
            'protocol_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'research_title': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site_leader': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bhp_research_protocol.SiteLeader']", 'symmetrical': 'False'})
        },
        'bhp_research_protocol.siteleader': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'SiteLeader'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_research_protocol']

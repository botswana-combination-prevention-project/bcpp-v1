# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Sponsor'
        db.create_table('bhp_research_protocol_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('contact_name', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('bhp_research_protocol', ['Sponsor'])

        # Adding model 'Funder'
        db.create_table('bhp_research_protocol_funder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('contact_name', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('contact_tel', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('bhp_research_protocol', ['Funder'])

        # Removing M2M table for field site on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_site')

        # Removing M2M table for field prinicipal_investigator on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_prinicipal_investigator')

        # Removing M2M table for field site_leader on 'Protocol'
        db.delete_table('bhp_research_protocol_protocol_site_leader')


    def backwards(self, orm):
        
        # Deleting model 'Sponsor'
        db.delete_table('bhp_research_protocol_sponsor')

        # Deleting model 'Funder'
        db.delete_table('bhp_research_protocol_funder')

        # Adding M2M table for field site on 'Protocol'
        db.create_table('bhp_research_protocol_protocol_site', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('protocol', models.ForeignKey(orm['bhp_research_protocol.protocol'], null=False)),
            ('site', models.ForeignKey(orm['bhp_research_protocol.site'], null=False))
        ))
        db.create_unique('bhp_research_protocol_protocol_site', ['protocol_id', 'site_id'])

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


    models = {
        'bhp_research_protocol.funder': {
            'Meta': {'ordering': "['name']", 'object_name': 'Funder'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'bhp_research_protocol.fundingsource': {
            'Meta': {'ordering': "['name']", 'object_name': 'FundingSource'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'bhp_research_protocol.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'bhp_research_protocol.principalinvestigator': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'PrincipalInvestigator'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
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
            'protocol_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'research_title': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site_name_fragment': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bhp_research_protocol.researchclinic': {
            'Meta': {'ordering': "['name']", 'object_name': 'ResearchClinic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'protocol': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_research_protocol.Protocol']", 'unique': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_research_protocol.Site']"})
        },
        'bhp_research_protocol.site': {
            'Meta': {'ordering': "['site_identifier']", 'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_research_protocol.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'site_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'})
        },
        'bhp_research_protocol.siteleader': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(['last_name', 'first_name'],)", 'object_name': 'SiteLeader'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_research_protocol.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bhp_research_protocol']

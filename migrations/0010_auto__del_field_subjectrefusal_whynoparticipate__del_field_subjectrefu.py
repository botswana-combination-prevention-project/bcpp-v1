# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'SubjectRefusal.whynoparticipate'
        db.delete_column('bcpp_subject_subjectrefusal', 'whynoparticipate')

        # Deleting field 'SubjectRefusal.hivtesttoday'
        db.delete_column('bcpp_subject_subjectrefusal', 'hivtesttoday')

        # Deleting field 'SubjectRefusal.whynoparticipate_other'
        db.delete_column('bcpp_subject_subjectrefusal', 'whynoparticipate_other')

        # Deleting field 'SubjectRefusal.lengthresidence'
        db.delete_column('bcpp_subject_subjectrefusal', 'lengthresidence')

        # Deleting field 'SubjectRefusal.whynohivtest'
        db.delete_column('bcpp_subject_subjectrefusal', 'whynohivtest')

        # Adding field 'SubjectRefusal.length_residence'
        db.add_column('bcpp_subject_subjectrefusal', 'length_residence', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.why_no_participate'
        db.add_column('bcpp_subject_subjectrefusal', 'why_no_participate', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.why_no_participate_other'
        db.add_column('bcpp_subject_subjectrefusal', 'why_no_participate_other', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True), keep_default=False)

        # Adding field 'SubjectRefusal.hiv_test_today'
        db.add_column('bcpp_subject_subjectrefusal', 'hiv_test_today', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.why_no_hivtest'
        db.add_column('bcpp_subject_subjectrefusal', 'why_no_hivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True), keep_default=False)

        # Deleting field 'PositiveParticipantAudit.familystigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'familystigma')

        # Deleting field 'PositiveParticipantAudit.enactedjobstigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enactedjobstigma')

        # Deleting field 'PositiveParticipantAudit.enactedtalkstigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enactedtalkstigma')

        # Deleting field 'PositiveParticipantAudit.internalize1stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'internalize1stigma')

        # Deleting field 'PositiveParticipantAudit.enactedrespectstigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enactedrespectstigma')

        # Deleting field 'PositiveParticipantAudit.friendstigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'friendstigma')

        # Deleting field 'PositiveParticipantAudit.internalized2stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'internalized2stigma')

        # Adding field 'PositiveParticipantAudit.internalize_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'internalize_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.internalized_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'internalized_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.friend_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'friend_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.family_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'family_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enacted_talk_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enacted_talk_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enacted_respect_stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enacted_respect_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enacted_jobs_tigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enacted_jobs_tigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'Stigma.enactedshamestigma'
        db.delete_column('bcpp_subject_stigma', 'enactedshamestigma')

        # Deleting field 'Stigma.teacherstigma'
        db.delete_column('bcpp_subject_stigma', 'teacherstigma')

        # Deleting field 'Stigma.childrenstigma'
        db.delete_column('bcpp_subject_stigma', 'childrenstigma')

        # Deleting field 'Stigma.salivastigma'
        db.delete_column('bcpp_subject_stigma', 'salivastigma')

        # Deleting field 'Stigma.anticipatestigma'
        db.delete_column('bcpp_subject_stigma', 'anticipatestigma')

        # Adding field 'Stigma.anticipate_stigma'
        db.add_column('bcpp_subject_stigma', 'anticipate_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.enacted_shame_stigma'
        db.add_column('bcpp_subject_stigma', 'enacted_shame_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.saliva_stigma'
        db.add_column('bcpp_subject_stigma', 'saliva_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.teacher_stigma'
        db.add_column('bcpp_subject_stigma', 'teacher_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.children_stigma'
        db.add_column('bcpp_subject_stigma', 'children_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'HivUntestedAudit.whynohivtest'
        db.delete_column('bcpp_subject_hivuntested_audit', 'whynohivtest')

        # Adding field 'HivUntestedAudit.why_no_hiv_test'
        db.add_column('bcpp_subject_hivuntested_audit', 'why_no_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True), keep_default=False)

        # Deleting field 'StigmaOpinionAudit.gossipcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'gossipcommunitystigma')

        # Deleting field 'StigmaOpinionAudit.enactedfamilystigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enactedfamilystigma')

        # Deleting field 'StigmaOpinionAudit.respectcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'respectcommunitystigma')

        # Deleting field 'StigmaOpinionAudit.fearstigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'fearstigma')

        # Deleting field 'StigmaOpinionAudit.enactedverbalstigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enactedverbalstigma')

        # Deleting field 'StigmaOpinionAudit.enactedphyicalstigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enactedphyicalstigma')

        # Deleting field 'StigmaOpinionAudit.testcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'testcommunitystigma')

        # Adding field 'StigmaOpinionAudit.test_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'test_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.gossip_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'gossip_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.respect_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'respect_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enacted_verbal_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enacted_verbal_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enacted_phyical_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enacted_phyical_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enacted_family_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enacted_family_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.fear_stigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'fear_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'PositiveParticipant.familystigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'familystigma')

        # Deleting field 'PositiveParticipant.enactedjobstigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enactedjobstigma')

        # Deleting field 'PositiveParticipant.enactedtalkstigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enactedtalkstigma')

        # Deleting field 'PositiveParticipant.internalize1stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'internalize1stigma')

        # Deleting field 'PositiveParticipant.internalized2stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'internalized2stigma')

        # Deleting field 'PositiveParticipant.enactedrespectstigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enactedrespectstigma')

        # Deleting field 'PositiveParticipant.friendstigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'friendstigma')

        # Adding field 'PositiveParticipant.internalize_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'internalize_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.internalized_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'internalized_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.friend_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'friend_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.family_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'family_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enacted_talk_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enacted_talk_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enacted_respect_stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enacted_respect_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enacted_jobs_tigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enacted_jobs_tigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'HivUntested.whynohivtest'
        db.delete_column('bcpp_subject_hivuntested', 'whynohivtest')

        # Adding field 'HivUntested.why_no_hiv_test'
        db.add_column('bcpp_subject_hivuntested', 'why_no_hiv_test', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True), keep_default=False)

        # Deleting field 'StigmaAudit.enactedshamestigma'
        db.delete_column('bcpp_subject_stigma_audit', 'enactedshamestigma')

        # Deleting field 'StigmaAudit.teacherstigma'
        db.delete_column('bcpp_subject_stigma_audit', 'teacherstigma')

        # Deleting field 'StigmaAudit.anticipatestigma'
        db.delete_column('bcpp_subject_stigma_audit', 'anticipatestigma')

        # Deleting field 'StigmaAudit.childrenstigma'
        db.delete_column('bcpp_subject_stigma_audit', 'childrenstigma')

        # Deleting field 'StigmaAudit.salivastigma'
        db.delete_column('bcpp_subject_stigma_audit', 'salivastigma')

        # Adding field 'StigmaAudit.anticipate_stigma'
        db.add_column('bcpp_subject_stigma_audit', 'anticipate_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.enacted_shame_stigma'
        db.add_column('bcpp_subject_stigma_audit', 'enacted_shame_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.saliva_stigma'
        db.add_column('bcpp_subject_stigma_audit', 'saliva_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.teacher_stigma'
        db.add_column('bcpp_subject_stigma_audit', 'teacher_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.children_stigma'
        db.add_column('bcpp_subject_stigma_audit', 'children_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'StigmaOpinion.gossipcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'gossipcommunitystigma')

        # Deleting field 'StigmaOpinion.enactedfamilystigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enactedfamilystigma')

        # Deleting field 'StigmaOpinion.respectcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'respectcommunitystigma')

        # Deleting field 'StigmaOpinion.fearstigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'fearstigma')

        # Deleting field 'StigmaOpinion.enactedverbalstigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enactedverbalstigma')

        # Deleting field 'StigmaOpinion.enactedphyicalstigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enactedphyicalstigma')

        # Deleting field 'StigmaOpinion.testcommunitystigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'testcommunitystigma')

        # Adding field 'StigmaOpinion.test_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'test_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.gossip_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'gossip_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.respect_community_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'respect_community_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enacted_verbal_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enacted_verbal_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enacted_phyical_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enacted_phyical_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enacted_family_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enacted_family_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.fear_stigma'
        db.add_column('bcpp_subject_stigmaopinion', 'fear_stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'SubjectRefusalAudit.whynoparticipate'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'whynoparticipate')

        # Deleting field 'SubjectRefusalAudit.hivtesttoday'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'hivtesttoday')

        # Deleting field 'SubjectRefusalAudit.whynoparticipate_other'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'whynoparticipate_other')

        # Deleting field 'SubjectRefusalAudit.lengthresidence'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'lengthresidence')

        # Deleting field 'SubjectRefusalAudit.whynohivtest'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'whynohivtest')

        # Adding field 'SubjectRefusalAudit.length_residence'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'length_residence', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.why_no_participate'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'why_no_participate', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.why_no_participate_other'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'why_no_participate_other', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True), keep_default=False)

        # Adding field 'SubjectRefusalAudit.hiv_test_today'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'hiv_test_today', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.why_no_hivtest'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'why_no_hivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'SubjectRefusal.whynoparticipate'
        db.add_column('bcpp_subject_subjectrefusal', 'whynoparticipate', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.hivtesttoday'
        db.add_column('bcpp_subject_subjectrefusal', 'hivtesttoday', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.whynoparticipate_other'
        db.add_column('bcpp_subject_subjectrefusal', 'whynoparticipate_other', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True), keep_default=False)

        # Adding field 'SubjectRefusal.lengthresidence'
        db.add_column('bcpp_subject_subjectrefusal', 'lengthresidence', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusal.whynohivtest'
        db.add_column('bcpp_subject_subjectrefusal', 'whynohivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True), keep_default=False)

        # Deleting field 'SubjectRefusal.length_residence'
        db.delete_column('bcpp_subject_subjectrefusal', 'length_residence')

        # Deleting field 'SubjectRefusal.why_no_participate'
        db.delete_column('bcpp_subject_subjectrefusal', 'why_no_participate')

        # Deleting field 'SubjectRefusal.why_no_participate_other'
        db.delete_column('bcpp_subject_subjectrefusal', 'why_no_participate_other')

        # Deleting field 'SubjectRefusal.hiv_test_today'
        db.delete_column('bcpp_subject_subjectrefusal', 'hiv_test_today')

        # Deleting field 'SubjectRefusal.why_no_hivtest'
        db.delete_column('bcpp_subject_subjectrefusal', 'why_no_hivtest')

        # Adding field 'PositiveParticipantAudit.familystigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'familystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enactedjobstigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enactedjobstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enactedtalkstigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enactedtalkstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.internalize1stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'internalize1stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.enactedrespectstigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'enactedrespectstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.friendstigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'friendstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipantAudit.internalized2stigma'
        db.add_column('bcpp_subject_positiveparticipant_audit', 'internalized2stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'PositiveParticipantAudit.internalize_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'internalize_stigma')

        # Deleting field 'PositiveParticipantAudit.internalized_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'internalized_stigma')

        # Deleting field 'PositiveParticipantAudit.friend_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'friend_stigma')

        # Deleting field 'PositiveParticipantAudit.family_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'family_stigma')

        # Deleting field 'PositiveParticipantAudit.enacted_talk_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enacted_talk_stigma')

        # Deleting field 'PositiveParticipantAudit.enacted_respect_stigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enacted_respect_stigma')

        # Deleting field 'PositiveParticipantAudit.enacted_jobs_tigma'
        db.delete_column('bcpp_subject_positiveparticipant_audit', 'enacted_jobs_tigma')

        # Adding field 'Stigma.enactedshamestigma'
        db.add_column('bcpp_subject_stigma', 'enactedshamestigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.teacherstigma'
        db.add_column('bcpp_subject_stigma', 'teacherstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.childrenstigma'
        db.add_column('bcpp_subject_stigma', 'childrenstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.salivastigma'
        db.add_column('bcpp_subject_stigma', 'salivastigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'Stigma.anticipatestigma'
        db.add_column('bcpp_subject_stigma', 'anticipatestigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'Stigma.anticipate_stigma'
        db.delete_column('bcpp_subject_stigma', 'anticipate_stigma')

        # Deleting field 'Stigma.enacted_shame_stigma'
        db.delete_column('bcpp_subject_stigma', 'enacted_shame_stigma')

        # Deleting field 'Stigma.saliva_stigma'
        db.delete_column('bcpp_subject_stigma', 'saliva_stigma')

        # Deleting field 'Stigma.teacher_stigma'
        db.delete_column('bcpp_subject_stigma', 'teacher_stigma')

        # Deleting field 'Stigma.children_stigma'
        db.delete_column('bcpp_subject_stigma', 'children_stigma')

        # Adding field 'HivUntestedAudit.whynohivtest'
        db.add_column('bcpp_subject_hivuntested_audit', 'whynohivtest', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True), keep_default=False)

        # Deleting field 'HivUntestedAudit.why_no_hiv_test'
        db.delete_column('bcpp_subject_hivuntested_audit', 'why_no_hiv_test')

        # Adding field 'StigmaOpinionAudit.gossipcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'gossipcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enactedfamilystigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enactedfamilystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.respectcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'respectcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.fearstigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'fearstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enactedverbalstigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enactedverbalstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.enactedphyicalstigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'enactedphyicalstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinionAudit.testcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion_audit', 'testcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'StigmaOpinionAudit.test_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'test_community_stigma')

        # Deleting field 'StigmaOpinionAudit.gossip_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'gossip_community_stigma')

        # Deleting field 'StigmaOpinionAudit.respect_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'respect_community_stigma')

        # Deleting field 'StigmaOpinionAudit.enacted_verbal_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enacted_verbal_stigma')

        # Deleting field 'StigmaOpinionAudit.enacted_phyical_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enacted_phyical_stigma')

        # Deleting field 'StigmaOpinionAudit.enacted_family_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'enacted_family_stigma')

        # Deleting field 'StigmaOpinionAudit.fear_stigma'
        db.delete_column('bcpp_subject_stigmaopinion_audit', 'fear_stigma')

        # Adding field 'PositiveParticipant.familystigma'
        db.add_column('bcpp_subject_positiveparticipant', 'familystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enactedjobstigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enactedjobstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enactedtalkstigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enactedtalkstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.internalize1stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'internalize1stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.internalized2stigma'
        db.add_column('bcpp_subject_positiveparticipant', 'internalized2stigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.enactedrespectstigma'
        db.add_column('bcpp_subject_positiveparticipant', 'enactedrespectstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'PositiveParticipant.friendstigma'
        db.add_column('bcpp_subject_positiveparticipant', 'friendstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'PositiveParticipant.internalize_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'internalize_stigma')

        # Deleting field 'PositiveParticipant.internalized_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'internalized_stigma')

        # Deleting field 'PositiveParticipant.friend_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'friend_stigma')

        # Deleting field 'PositiveParticipant.family_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'family_stigma')

        # Deleting field 'PositiveParticipant.enacted_talk_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enacted_talk_stigma')

        # Deleting field 'PositiveParticipant.enacted_respect_stigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enacted_respect_stigma')

        # Deleting field 'PositiveParticipant.enacted_jobs_tigma'
        db.delete_column('bcpp_subject_positiveparticipant', 'enacted_jobs_tigma')

        # Adding field 'HivUntested.whynohivtest'
        db.add_column('bcpp_subject_hivuntested', 'whynohivtest', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True), keep_default=False)

        # Deleting field 'HivUntested.why_no_hiv_test'
        db.delete_column('bcpp_subject_hivuntested', 'why_no_hiv_test')

        # Adding field 'StigmaAudit.enactedshamestigma'
        db.add_column('bcpp_subject_stigma_audit', 'enactedshamestigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.teacherstigma'
        db.add_column('bcpp_subject_stigma_audit', 'teacherstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.anticipatestigma'
        db.add_column('bcpp_subject_stigma_audit', 'anticipatestigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.childrenstigma'
        db.add_column('bcpp_subject_stigma_audit', 'childrenstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaAudit.salivastigma'
        db.add_column('bcpp_subject_stigma_audit', 'salivastigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'StigmaAudit.anticipate_stigma'
        db.delete_column('bcpp_subject_stigma_audit', 'anticipate_stigma')

        # Deleting field 'StigmaAudit.enacted_shame_stigma'
        db.delete_column('bcpp_subject_stigma_audit', 'enacted_shame_stigma')

        # Deleting field 'StigmaAudit.saliva_stigma'
        db.delete_column('bcpp_subject_stigma_audit', 'saliva_stigma')

        # Deleting field 'StigmaAudit.teacher_stigma'
        db.delete_column('bcpp_subject_stigma_audit', 'teacher_stigma')

        # Deleting field 'StigmaAudit.children_stigma'
        db.delete_column('bcpp_subject_stigma_audit', 'children_stigma')

        # Adding field 'StigmaOpinion.gossipcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion', 'gossipcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enactedfamilystigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enactedfamilystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.respectcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion', 'respectcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.fearstigma'
        db.add_column('bcpp_subject_stigmaopinion', 'fearstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enactedverbalstigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enactedverbalstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.enactedphyicalstigma'
        db.add_column('bcpp_subject_stigmaopinion', 'enactedphyicalstigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Adding field 'StigmaOpinion.testcommunitystigma'
        db.add_column('bcpp_subject_stigmaopinion', 'testcommunitystigma', self.gf('django.db.models.fields.CharField')(default=0, max_length=25), keep_default=False)

        # Deleting field 'StigmaOpinion.test_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'test_community_stigma')

        # Deleting field 'StigmaOpinion.gossip_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'gossip_community_stigma')

        # Deleting field 'StigmaOpinion.respect_community_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'respect_community_stigma')

        # Deleting field 'StigmaOpinion.enacted_verbal_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enacted_verbal_stigma')

        # Deleting field 'StigmaOpinion.enacted_phyical_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enacted_phyical_stigma')

        # Deleting field 'StigmaOpinion.enacted_family_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'enacted_family_stigma')

        # Deleting field 'StigmaOpinion.fear_stigma'
        db.delete_column('bcpp_subject_stigmaopinion', 'fear_stigma')

        # Adding field 'SubjectRefusalAudit.whynoparticipate'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'whynoparticipate', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.hivtesttoday'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'hivtesttoday', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.whynoparticipate_other'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'whynoparticipate_other', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True), keep_default=False)

        # Adding field 'SubjectRefusalAudit.lengthresidence'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'lengthresidence', self.gf('django.db.models.fields.CharField')(default=0, max_length=15), keep_default=False)

        # Adding field 'SubjectRefusalAudit.whynohivtest'
        db.add_column('bcpp_subject_subjectrefusal_audit', 'whynohivtest', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True), keep_default=False)

        # Deleting field 'SubjectRefusalAudit.length_residence'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'length_residence')

        # Deleting field 'SubjectRefusalAudit.why_no_participate'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'why_no_participate')

        # Deleting field 'SubjectRefusalAudit.why_no_participate_other'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'why_no_participate_other')

        # Deleting field 'SubjectRefusalAudit.hiv_test_today'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'hiv_test_today')

        # Deleting field 'SubjectRefusalAudit.why_no_hivtest'
        db.delete_column('bcpp_subject_subjectrefusal_audit', 'why_no_hivtest')


    models = {
        'bcpp_household.contactlog': {
            'Meta': {'object_name': 'ContactLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.gpsdevice': {
            'Meta': {'object_name': 'GpsDevice'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gps_make': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gps_model': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gps_purchase_date': ('django.db.models.fields.DateField', [], {}),
            'gps_purchase_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'gps_serial_number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_household.household': {
            'Meta': {'ordering': "['-household_identifier']", 'object_name': 'Household'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'cso_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'gps_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'gps_device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.GpsDevice']"}),
            'gps_point_1': ('django.db.models.fields.CharField', [], {'default': '24', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_11': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_point_2': ('django.db.models.fields.CharField', [], {'default': '26', 'max_length': '78L', 'db_index': 'True'}),
            'gps_point_21': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gps_waypoint': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hh_int': ('django.db.models.fields.IntegerField', [], {}),
            'hh_seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_map': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'ward': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.Ward']", 'unique': 'True'}),
            'ward_section': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'was_surveyed_previously': ('django.db.models.fields.CharField', [], {'default': "'No'", 'max_length': '10'})
        },
        'bcpp_household.householdstructure': {
            'Meta': {'unique_together': "(('household', 'survey'),)", 'object_name': 'HouseholdStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.Household']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.householdstructuremember': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('household_structure', 'first_name', 'initials'), ('registered_subject', 'household_structure'))", 'object_name': 'HouseholdStructureMember'},
            'age_in_years': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact_log': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.ContactLog']", 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'hiv_history': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_household.HouseholdStructure']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'is_eligible_member': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'lives_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'member_status': ('django.db.models.fields.CharField', [], {'default': "'NOT_REPORTED'", 'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'target': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_household.ward': {
            'Meta': {'object_name': 'Ward'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'ward_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'db_index': 'True'})
        },
        'bcpp_list.circumcisionbenefits': {
            'Meta': {'object_name': 'CircumcisionBenefits'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.electricalappliances': {
            'Meta': {'object_name': 'ElectricalAppliances'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.familyplanning': {
            'Meta': {'object_name': 'FamilyPlanning'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.heartdisease': {
            'Meta': {'object_name': 'HeartDisease'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.livewith': {
            'Meta': {'object_name': 'LiveWith'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.medicalcareaccess': {
            'Meta': {'object_name': 'MedicalCareAccess'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.neighbourhoodproblems': {
            'Meta': {'object_name': 'NeighbourhoodProblems'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.partnerresidency': {
            'Meta': {'object_name': 'PartnerResidency'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.subjectabsenteereason': {
            'Meta': {'object_name': 'SubjectAbsenteeReason'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.surveygroup': {
            'Meta': {'object_name': 'SurveyGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_list.transportmode': {
            'Meta': {'object_name': 'TransportMode'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bcpp_subject.accesstocare': {
            'Meta': {'object_name': 'AccessToCare'},
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_care_access': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.MedicalCareAccess']", 'symmetrical': 'False'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.accesstocareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'AccessToCareAudit', 'db_table': "'bcpp_subject_accesstocare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'access_care': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'access_care_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'convenient_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'emergency_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'expensive_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_care_access_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'overall_access': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_accesstocare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'whenever_access': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.baselinehouseholdsurvey': {
            'Meta': {'object_name': 'BaselineHouseholdSurvey'},
            'cattle_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'electrical_appliances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.ElectricalAppliances']", 'null': 'True', 'blank': 'True'}),
            'energy_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'energy_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'flooring_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'flooring_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'goats_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'transport_mode': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.TransportMode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.baselinehouseholdsurveyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'BaselineHouseholdSurveyAudit', 'db_table': "'bcpp_subject_baselinehouseholdsurvey_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cattle_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'energy_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'energy_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'flooring_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'flooring_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'goats_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'living_rooms': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'sheep_owned': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'smaller_meals': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_baselinehouseholdsurvey'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'toilet_facility': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'toilet_facility_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'water_source': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'water_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.ceaenrolmentchecklist': {
            'Meta': {'object_name': 'CeaEnrolmentChecklist'},
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrolment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.ceaenrolmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CeaEnrolmentChecklistAudit', 'db_table': "'bcpp_subject_ceaenrolmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cd4_count': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cd4_date': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'diagnosis_date': ('django.db.models.fields.DateField', [], {'max_length': '3'}),
            'enrolment_reason': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'opportunistic_illness': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_ceaenrolmentchecklist'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcised': {
            'Meta': {'object_name': 'Circumcised'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.CircumcisionBenefits']", 'max_length': '25', 'symmetrical': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.circumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisedAudit', 'db_table': "'bcpp_subject_circumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'when_circ': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'where_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'why_circ': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'why_circ_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.circumcision': {
            'Meta': {'object_name': 'Circumcision'},
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.circumcisionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CircumcisionAudit', 'db_table': "'bcpp_subject_circumcision_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_circumcision'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.communityengagement': {
            'Meta': {'object_name': 'CommunityEngagement'},
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.NeighbourhoodProblems']", 'symmetrical': 'False'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.communityengagementaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CommunityEngagementAudit', 'db_table': "'bcpp_subject_communityengagement_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'community_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problems_engagement_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'solve_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_communityengagement'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'vote_engagement': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.csenrolmentchecklist': {
            'Meta': {'object_name': 'CsEnrolmentChecklist'},
            'census_number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_consent_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'date_guardian_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'date_minor_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.csenrolmentchecklistaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CsEnrolmentChecklistAudit', 'db_table': "'bcpp_subject_csenrolmentchecklist_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'census_number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'citizen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'community_resident': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_consent_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25'}),
            'date_guardian_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'date_minor_signed': ('django.db.models.fields.DateTimeField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'incarceration': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mental_capacity': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_csenrolmentchecklist'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'live_with': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.LiveWith']", 'null': 'True', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.demographicsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'DemographicsAudit', 'db_table': "'bcpp_subject_demographics_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_wives': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'religion_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_demographics'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.education': {
            'Meta': {'object_name': 'Education'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'employment': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_forwork': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'seeking_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.educationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'EducationAudit', 'db_table': "'bcpp_subject_education_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'employment': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_forwork': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'seeking_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_education'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.futurehivtesting': {
            'Meta': {'object_name': 'FutureHivTesting'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.futurehivtestingaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'FutureHivTestingAudit', 'db_table': "'bcpp_subject_futurehivtesting_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_time': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_time_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_week': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hiv_test_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_test_year': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hiv_test_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prefer_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_futurehivtesting'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grant': {
            'Meta': {'object_name': 'Grant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.grantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'GrantAudit', 'db_table': "'bcpp_subject_grant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grant_number': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'grant_type': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'labour_market_wages': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_grant'", 'to': "orm['bcpp_subject.LabourMarketWages']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_grant': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivcareadherence': {
            'Meta': {'object_name': 'HivCareAdherence'},
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivcareadherenceaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivCareAdherenceAudit', 'db_table': "'bcpp_subject_hivcareadherence_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'adherence_4_day': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'adherence_4_wk': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'arv_naive': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'arv_stop': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'arv_stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'arv_stop_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_recommended_arv': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_arv': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_positive': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_care': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'no_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'on_arv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivcareadherence'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_arv': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'why_no_arv_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.hivhealthcarecosts': {
            'Meta': {'object_name': 'HivHealthCareCosts'},
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivhealthcarecostsaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivHealthCareCostsAudit', 'db_table': "'bcpp_subject_hivhealthcarecosts_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_regularity': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doctor_visits': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hiv_medical_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'place_care_received': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reason_no_care': ('django.db.models.fields.CharField', [], {'max_length': '115', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivhealthcarecosts'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcare': {
            'Meta': {'object_name': 'HivMedicalCare'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivmedicalcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivMedicalCareAudit', 'db_table': "'bcpp_subject_hivmedicalcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_hiv_care_pos': ('django.db.models.fields.DateField', [], {'max_length': '25'}),
            'lowest_cd4': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivmedicalcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hivtested': {
            'Meta': {'object_name': 'HivTested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestedAudit', 'db_table': "'bcpp_subject_hivtested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'num_hiv_tests': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '85', 'null': 'True', 'blank': 'True'}),
            'why_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '105', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestinghistory': {
            'Meta': {'object_name': 'HivTestingHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestinghistoryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestingHistoryAudit', 'db_table': "'bcpp_subject_hivtestinghistory_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_record': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'has_tested': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestinghistory'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_not_tested': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivtestreview': {
            'Meta': {'object_name': 'HivTestReview'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.hivtestreviewaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivTestReviewAudit', 'db_table': "'bcpp_subject_hivtestreview_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'recorded_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivtestreview'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'verbal_hiv_result': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'when_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.hivuntested': {
            'Meta': {'object_name': 'HivUntested'},
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hivuntestedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HivUntestedAudit', 'db_table': "'bcpp_subject_hivuntested_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'arvs_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_pills': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hivuntested'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hiv_test': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.hospitaladmission': {
            'Meta': {'object_name': 'HospitalAdmission'},
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.hospitaladmissionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HospitalAdmissionAudit', 'db_table': "'bcpp_subject_hospitaladmission_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'admission_nights': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'facility_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'healthcare_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'hospitalization_costs': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reason_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_hospitaladmission'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'total_expenses': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'travel_hours': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.householdcomposition': {
            'Meta': {'object_name': 'HouseholdComposition'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'housecode': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {'max_length': '25'}),
            'physical_add': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.householdcompositionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'HouseholdCompositionAudit', 'db_table': "'bcpp_subject_householdcomposition_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'housecode': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {'max_length': '25'}),
            'physical_add': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_householdcomposition'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.labourmarketwages': {
            'Meta': {'object_name': 'LabourMarketWages'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.labourmarketwagesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'LabourMarketWagesAudit', 'db_table': "'bcpp_subject_labourmarketwages_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_inactivite': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_not_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'days_worked': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'employed': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'govt_grant': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_income': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'job_description_change': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'monthly_income': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'nights_out': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'other_occupation': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'other_occupation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'salary_payment': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_labourmarketwages'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'weeks_out': ('django.db.models.fields.CharField', [], {'max_length': '17'})
        },
        'bcpp_subject.medicaldiagnoses': {
            'Meta': {'object_name': 'MedicalDiagnoses'},
            'cancer': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'dx_heart_attack': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bcpp_list.HeartDisease']", 'null': 'True', 'blank': 'True'}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'heart_attack': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'sti': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'tb': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.medicaldiagnosesaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MedicalDiagnosesAudit', 'db_table': "'bcpp_subject_medicaldiagnoses_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cancer': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'cancer_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_cancer': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_heart_attack': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_tb': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dx_cancer': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'dx_tb': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'heart_attack': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'heart_attack_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'sti': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_medicaldiagnoses'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'tb': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tb_record': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartner': {
            'Meta': {'object_name': 'MonthsRecentPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsrecentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsRecentPartnerAudit', 'db_table': "'bcpp_subject_monthsrecentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsrecentpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartner': {
            'Meta': {'object_name': 'MonthsSecondPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthssecondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsSecondPartnerAudit', 'db_table': "'bcpp_subject_monthssecondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthssecondpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartner': {
            'Meta': {'object_name': 'MonthsThirdPartner'},
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_live': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.PartnerResidency']", 'symmetrical': 'False'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.monthsthirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'MonthsThirdPartnerAudit', 'db_table': "'bcpp_subject_monthsthirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'concurrent': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_condom_freq': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_disclose': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'first_exchange': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'first_first_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_first_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_haart': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_partner_cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_partner_hiv': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_relationship': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'first_sex_current': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex_freq': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'goods_exchange': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_monthsthirdpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'third_last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'third_last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.outpatientcare': {
            'Meta': {'object_name': 'OutpatientCare'},
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.outpatientcareaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'OutpatientCareAudit', 'db_table': "'bcpp_subject_outpatientcare_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'care_reason': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'care_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'care_visits': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'cost_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dept_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'facility_visited': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'govt_health_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'outpatient_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'prvt_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'specific_clinic': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_outpatientcare'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'trad_care': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'transport_expense': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'travel_time': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'waiting_hours': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'bcpp_subject.positiveparticipant': {
            'Meta': {'object_name': 'PositiveParticipant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.positiveparticipantaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'PositiveParticipantAudit', 'db_table': "'bcpp_subject_positiveparticipant_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_jobs_tigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_respect_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_talk_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'friend_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'internalize_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'internalized_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_positiveparticipant'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.qualityoflife': {
            'Meta': {'object_name': 'QualityOfLife'},
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.qualityoflifeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'QualityOfLifeAudit', 'db_table': "'bcpp_subject_qualityoflife_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'anxiety': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'health_today': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'mobility': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'pain': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'self_care': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_qualityoflife'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.recentpartner': {
            'Meta': {'object_name': 'RecentPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.recentpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'RecentPartnerAudit', 'db_table': "'bcpp_subject_recentpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_recentpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.reproductivehealth': {
            'Meta': {'object_name': 'ReproductiveHealth'},
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_planning': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.FamilyPlanning']", 'symmetrical': 'False'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lnmp': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'bcpp_subject.reproductivehealthaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReproductiveHealthAudit', 'db_table': "'bcpp_subject_reproductivehealth_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anc_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'anc_reg': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'current_pregnant': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'family_planning_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'hiv_last_pregnancy': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lnmp': ('django.db.models.fields.DateField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_children': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'number_children': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'preg_arv': ('django.db.models.fields.CharField', [], {'max_length': '95', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_reproductivehealth'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'where_circ': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'bcpp_subject.residencymobility': {
            'Meta': {'object_name': 'ResidencyMobility'},
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'forteen_nights': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'reason_away': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reason_away_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.residencymobilityaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResidencyMobilityAudit', 'db_table': "'bcpp_subject_residencymobility_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'cattle_postlands': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'cattle_postlands_other': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'forteen_nights': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intend_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_away': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'reason_away': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reason_away_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_residencymobility'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilization': {
            'Meta': {'object_name': 'ResourceUtilization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.resourceutilizationaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ResourceUtilizationAudit', 'db_table': "'bcpp_subject_resourceutilization_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hospitalized': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'medical_cover': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'money_spent': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'out_patient': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_resourceutilization'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.respondent': {
            'Meta': {'object_name': 'Respondent'},
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_composition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.HouseholdComposition']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_outside': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.respondentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'RespondentAudit', 'db_table': "'bcpp_subject_respondent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_composition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_respondent'", 'to': "orm['bcpp_subject.HouseholdComposition']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nights_outside': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'present': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relation_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.secondpartner': {
            'Meta': {'object_name': 'SecondPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.secondpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SecondPartnerAudit', 'db_table': "'bcpp_subject_secondpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_secondpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviour': {
            'Meta': {'object_name': 'SexualBehaviour'},
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.sexualbehaviouraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SexualBehaviourAudit', 'db_table': "'bcpp_subject_sexualbehaviour_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'condom': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ever_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'first_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'last_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_calc': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'last_year_partners': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'more_sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_sexualbehaviour'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigma': {
            'Meta': {'object_name': 'Stigma'},
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaAudit', 'db_table': "'bcpp_subject_stigma_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'anticipate_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'children_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_shame_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'saliva_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigma'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'teacher_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinion': {
            'Meta': {'object_name': 'StigmaOpinion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.stigmaopinionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'StigmaOpinionAudit', 'db_table': "'bcpp_subject_stigmaopinion_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enacted_family_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_phyical_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'enacted_verbal_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'fear_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'gossip_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'respect_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_stigmaopinion'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'test_community_stigma': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsentee': {
            'Meta': {'unique_together': "(('registered_subject', 'survey'),)", 'object_name': 'SubjectAbsentee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructureMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeAudit', 'db_table': "'bcpp_subject_subjectabsentee_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'to': "orm['bcpp_household.HouseholdStructureMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsentee'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeentry': {
            'Meta': {'unique_together': "(('subject_absentee', 'report_datetime'),)", 'object_name': 'SubjectAbsenteeEntry'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_absentee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectAbsentee']"}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SubjectAbsenteeReason']", 'null': 'True'}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteeentryaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeEntryAudit', 'db_table': "'bcpp_subject_subjectabsenteeentry_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_absentee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteeentry'", 'to': "orm['bcpp_subject.SubjectAbsentee']"}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteeentry'", 'null': 'True', 'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteereport': {
            'Meta': {'object_name': 'SubjectAbsenteeReport'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectabsenteereportaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectAbsenteeReportAudit', 'db_table': "'bcpp_subject_subjectabsenteereport_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'next_appt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'next_appt_datetime_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'subject_absentee_reason': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteereport'", 'to': "orm['bcpp_list.SubjectAbsenteeReason']"}),
            'subject_absentee_reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'subject_absentee_status': ('django.db.models.fields.CharField', [], {'default': "'absent'", 'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectabsenteereport'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectconsent': {
            'Meta': {'object_name': 'SubjectConsent'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructureMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectconsentaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectConsentAudit', 'db_table': "'bcpp_subject_subjectconsent_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_household.HouseholdStructureMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_minor': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '10', 'null': 'True'}),
            'is_signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectconsent'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'bcpp_subject.subjectdeath': {
            'Meta': {'object_name': 'SubjectDeath'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_adverse.DeathReasonHospitalized']", 'null': 'True', 'blank': 'True'}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectdeathaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectDeathAudit', 'db_table': "'bcpp_subject_subjectdeath_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days_decedent_hospitalized': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_hospitalized': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'death_cause': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'death_cause_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_adverse.DeathCauseCategory']"}),
            'death_cause_info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_adverse.DeathCauseInfo']"}),
            'death_cause_info_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_cause_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            'death_reason_hospitalized': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_audit_subjectdeath'", 'null': 'True', 'to': "orm['bhp_adverse.DeathReasonHospitalized']"}),
            'death_year': ('django.db.models.fields.DateField', [], {}),
            'decedent_haart': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'decedent_haart_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decedent_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'decendent_death_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'doctor_evaluation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'document_community': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'document_community_other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'document_hiv': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_death': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hospital_visits': ('django.db.models.fields.IntegerField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'participant_hospitalized': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectdeath'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'sufficient_records': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocator': {
            'Meta': {'object_name': 'SubjectLocator'},
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 7, 2)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 436981)'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'null': 'True'}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectlocatoraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectLocatorAudit', 'db_table': "'bcpp_subject_subjectlocator_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_cell_number': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'alt_contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2013, 7, 2)'}),
            'has_alt_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'other_alt_contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 436981)'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectlocator'", 'null': 'True', 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectmoved': {
            'Meta': {'ordering': "['household_structure_member']", 'object_name': 'SubjectMoved'},
            'area_moved': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructureMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'moved_date': ('django.db.models.fields.DateField', [], {}),
            'moved_reason': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'moved_reason_other': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'place_moved': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectmovedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectMovedAudit', 'db_table': "'bcpp_subject_subjectmoved_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'area_moved': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_details': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'to': "orm['bcpp_household.HouseholdStructureMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'moved_date': ('django.db.models.fields.DateField', [], {}),
            'moved_reason': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'moved_reason_other': ('django.db.models.fields.TextField', [], {'max_length': '250', 'blank': 'True'}),
            'place_moved': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectmoved'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudy': {
            'Meta': {'object_name': 'SubjectOffStudy'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectoffstudyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectOffStudyAudit', 'db_table': "'bcpp_subject_subjectoffstudy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectoffstudy'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectrefusal': {
            'Meta': {'ordering': "['household_structure_member']", 'object_name': 'SubjectRefusal'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_household.HouseholdStructureMember']", 'unique': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'refusal_date': ('django.db.models.fields.DateField', [], {}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_refusal_status': ('django.db.models.fields.CharField', [], {'default': "'REFUSED'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'why_no_participate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'why_no_participate_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.subjectrefusalaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectRefusalAudit', 'db_table': "'bcpp_subject_subjectrefusal_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hiv_test_today': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'household_structure_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'to': "orm['bcpp_household.HouseholdStructureMember']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'length_residence': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'refusal_date': ('django.db.models.fields.DateField', [], {}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'null': 'True', 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 841015)'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_refusal_status': ('django.db.models.fields.CharField', [], {'default': "'REFUSED'", 'max_length': '25'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectrefusal'", 'to': "orm['bcpp_survey.Survey']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'why_no_hivtest': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'why_no_participate': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'why_no_participate_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'})
        },
        'bcpp_subject.subjectvisit': {
            'Meta': {'object_name': 'SubjectVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bhp_appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.subjectvisitaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubjectVisitAudit', 'db_table': "'bcpp_subject_subjectvisit_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_subjectvisit'", 'to': "orm['bhp_appointment.Appointment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'reason_unscheduled': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuse': {
            'Meta': {'object_name': 'SubstanceUse'},
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.substanceuseaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'SubstanceUseAudit', 'db_table': "'bcpp_subject_substanceuse_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'smoke': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_substanceuse'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.thirdpartner': {
            'Meta': {'object_name': 'ThirdPartner'},
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.thirdpartneraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ThirdPartnerAudit', 'db_table': "'bcpp_subject_thirdpartner_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'alcohol_before_sex': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'first_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'having_sex': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'having_sex_reg': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'intercourse_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'last_sex_contact': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'last_sex_contact_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'multiple_partners': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'partner_arv': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'partner_gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'partner_residency': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'partner_status': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'regular_sex': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'rel_type_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'status_disclosure': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_thirdpartner'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcised': {
            'Meta': {'object_name': 'Uncircumcised'},
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_week': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_year': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'health_benefits_smc': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bcpp_list.CircumcisionBenefits']", 'max_length': '25', 'symmetrical': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bcpp_subject.SubjectVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_subject.uncircumcisedaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'UncircumcisedAudit', 'db_table': "'bcpp_subject_uncircumcised_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aware_free': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'circumcised': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_day_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_week': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_week_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'circumcision_year': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'circumcision_year_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'future_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'future_reasons_smc': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason_circ': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 2, 16, 28, 0, 714884)'}),
            'service_facilities': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'subject_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_uncircumcised'", 'to': "orm['bcpp_subject.SubjectVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bcpp_survey.survey': {
            'Meta': {'ordering': "['survey_name']", 'unique_together': "(('survey_name', 'survey_group'), ('survey_group', 'chronological_order'))", 'object_name': 'Survey'},
            'chronological_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'survey_description': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'survey_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcpp_list.SurveyGroup']"}),
            'survey_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'survey_slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_adverse.deathcausecategory': {
            'Meta': {'ordering': "['display_index']", 'object_name': 'DeathCauseCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'bhp_appointment.appointment': {
            'Meta': {'ordering': "['registered_subject', 'appt_datetime']", 'unique_together': "(('registered_subject', 'visit_definition', 'visit_instance'),)", 'object_name': 'Appointment'},
            'appt_close_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25', 'db_index': 'True'}),
            'appt_type': ('django.db.models.fields.CharField', [], {'default': "'clinic'", 'max_length': '20'}),
            'best_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dashboard_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['bhp_registration.RegisteredSubject']"}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'timepoint_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['bhp_visit.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'bhp_content_type_map.contenttypemap': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap', 'db_table': "'bhp_common_contenttypemap'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials'),)", 'object_name': 'RegisteredSubject'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_visit.membershipform': {
            'Meta': {'object_name': 'MembershipForm'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '25', 'null': 'True'}),
            'content_type_map': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'bhp_visit.schedulegroup': {
            'Meta': {'ordering': "['group_name']", 'object_name': 'ScheduleGroup'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'grouping_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'membership_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_visit.MembershipForm']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_visit.visitdefinition': {
            'Meta': {'ordering': "['code', 'time_point']", 'object_name': 'VisitDefinition'},
            'base_interval': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'base_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'melissa'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'lower_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lower_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'schedule_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bhp_visit.ScheduleGroup']", 'null': 'True', 'blank': 'True'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_index': 'True'}),
            'upper_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upper_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_tracking_content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bcpp_subject']

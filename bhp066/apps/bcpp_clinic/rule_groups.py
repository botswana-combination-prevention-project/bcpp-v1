from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, Logic, ScheduledDataRule, RequisitionRule

from .models import ClinicVisit, ViralLoadTracking, Questionnaire


class InitiationRequisitionRuleGroup(RuleGroup):

    initiation = RequisitionRule(
        logic=Logic(
            predicate=(('registration_type', 'equals', 'Initiation Visit'), ('registration_type', 'equals', 'Other NON-VL Visit', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'clinicrequisition')],
        target_requisition_panels=['Clinic Viral Load'],)

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = Questionnaire
site_rule_groups.register(InitiationRequisitionRuleGroup)


class MasaRuleGroup(RuleGroup):
    '''confirms visit reason before
    updating the VL tracking scheduled metadata status to NEW.'''
    is_drawn = ScheduledDataRule(
        logic=Logic(
            predicate=(('registration_type', 'equals', 'MASA Scheduled VL Visit'), ('registration_type', 'equals', 'CCC visit', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=['viralloadtracking'])

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = Questionnaire
site_rule_groups.register(MasaRuleGroup)


class ViralLoadTrackingRuleGroup(RuleGroup):

    is_drawn = ScheduledDataRule(
        logic=Logic(
            predicate=('is_drawn', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['clinicvlresult'])

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = ViralLoadTracking
site_rule_groups.register(ViralLoadTrackingRuleGroup)

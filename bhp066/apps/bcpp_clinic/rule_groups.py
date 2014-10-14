from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, Logic, ScheduledDataRule  # ,RequisitionRule

from .models import ClinicVisit, ViralLoadTracking


class ViralLoadTrackingRuleGroup(RuleGroup):

    is_drawn = ScheduledDataRule(
        logic=Logic(
            predicate=('is_drawn', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['viralloadresult'])

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = ViralLoadTracking
site_rule_groups.register(ViralLoadTrackingRuleGroup)

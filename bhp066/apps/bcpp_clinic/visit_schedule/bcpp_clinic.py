from ..models import ClinicVisit, ClinicConsent

from collections import OrderedDict

from edc.constants import REQUIRED, NOT_ADDITIONAL, ADDITIONAL, NOT_REQUIRED
from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionPanelTuple


class BcppClinicVisitSchedule(VisitScheduleConfiguration):

    name = 'clinic visit schedule'
    app_label = 'bcpp_clinic'
    panel_model = 'Panel'
    membership_forms = OrderedDict({
        'clinic': MembershipFormTuple('clinic', ClinicConsent, True),
        })

    # schedule groups
    # (name, membership_form_name, grouping_key, comment)
    schedule_groups = OrderedDict({
        'group-2': ScheduleGroupTuple('group-2', 'clinic', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'C0': {
            'title': 'Clinic Registration',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': ClinicVisit,
            'schedule_group': 'group-2',
            'instructions': None,
            'requisitions': (
#               # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type) OLD
                RequisitionPanelTuple(10L, u'bcpp_lab', u'clinicrequisition', 'Research Blood Draw', 'TEST', 'WB', REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(20L, u'bcpp_lab', u'clinicrequisition', 'Viral Load', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
                ),
            'entries': (
            EntryTuple(10L, u'bcpp_clinic', u'clinicsubjectlocator', REQUIRED, NOT_ADDITIONAL,),
            EntryTuple(20L, u'bcpp_clinic', u'clinicquestionnaire', REQUIRED, NOT_ADDITIONAL,),
            EntryTuple(30L, u'bcpp_clinic', u'clinicvlresult', NOT_REQUIRED, ADDITIONAL,),
            EntryTuple(40L, u'bcpp_clinic', u'viralloadtracking', NOT_REQUIRED, ADDITIONAL,),
            )}
        }
    )

site_visit_schedules.register(BcppClinicVisitSchedule)

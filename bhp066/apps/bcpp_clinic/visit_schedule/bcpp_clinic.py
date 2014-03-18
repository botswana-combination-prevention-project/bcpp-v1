from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionPanelTuple

from apps.bcpp_lab.models import Panel, AliquotType

from ..models import ClinicVisit, ClinicEligibility


class BcppClinicVisitSchedule(VisitScheduleConfiguration):

    name = 'clinic visit schedule'
    app_label = 'bcpp_clinic'
    panel_model = Panel
    aliquot_type_model = AliquotType
    # membership forms
    # (name, model, visible)
    membership_forms = OrderedDict({
        'clinic': MembershipFormTuple('clinic', ClinicEligibility, True),
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
            'title': 'C0',
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
                # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type)
                RequisitionPanelTuple(10L, u'bcpp_clinic_lab', u'clinicrequisition', 'Research Blood Draw', 'TEST', 'WB'),
                RequisitionPanelTuple(20L, u'bcpp_clinic_lab', u'clinicrequisition', 'Viral Load', 'TEST', 'WB'),
                ),
            'entries': (
                EntryTuple(10L, u'bcpp_clinic', u'clinicmain'),
            )}
        }
    )

site_visit_schedules.register(BcppClinicVisitSchedule)

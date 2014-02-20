from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionTuple

from apps.bcpp_rbd_subject.models import SubjectVisitRBD, SubjectConsentRBDonly


class BcppRBDSubjectVisitSchedule(VisitScheduleConfiguration):

    name = 'visit schedule'
    app_label = 'bcpp_rbd_subject'
    # membership forms
    # (name, model, visible)
    membership_forms = OrderedDict({
        'subject_rbd-year-1': MembershipFormTuple('subject_rbd-year-1', SubjectConsentRBDonly, True),
        })

    # schedule groups
    # (name, membership_form_name, grouping_key, comment)
    schedule_groups = OrderedDict({
        'group-3': ScheduleGroupTuple('group-3', 'subject_rbd-year-1', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'R0': {
            'title': 'R0',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': SubjectVisitRBD,
            'schedule_group': 'group-3',
            'instructions': None,
            'requisitions': (
                # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type)
                RequisitionTuple(10L, u'bcpp_lab', u'rbdsubjectRequisition', 'Research Blood Draw', 'Research Blood Draw', 'TEST', 'WB'),
                ),
            'entries': (
                EntryTuple(10L, u'bcpp_rbd_subject', u'subjectlocatorrbd'),
                EntryTuple(20L, u'bcpp_rbd_subject', u'rbddemographics'),
            )}
        }
    )

site_visit_schedules.register(BcppRBDSubjectVisitSchedule)

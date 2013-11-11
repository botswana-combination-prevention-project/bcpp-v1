from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules

from ..models import SubjectVisit, SubjectConsent


class BcppSubjectVisitSchedule(VisitScheduleConfiguration):

    app_label = 'bcpp_subject'
    # membership forms
    # see edc.subject.visit_schedule.models.membership_forms
    membership_forms = OrderedDict({
        'bcpp-year-1': ('bcpp-year-1', SubjectConsent, True),
        })

    # schedule groups
    # see edc.subject.visit_schedule.models.schedule_groups
    # (group_name, membership_form, grouping_key, comment)
    schedule_groups = OrderedDict({
        'bcpp-year-1': ('bcpp-year-1', 'bcpp-year-1', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'T0': {
            'title': 'T0',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': SubjectVisit,
            'schedule_group': 'bcpp-year-1',
            'instructions': None,
            'entries': (
                (10L, u'bcpp_subject', u'subjectlocator'),
                (20L, u'bcpp_subject', u'residencymobility'),
                (30L, u'bcpp_subject', u'communityengagement'),
                (40L, u'bcpp_subject', u'demographics'),
                (50L, u'bcpp_subject', u'education'),
                (60L, u'bcpp_subject', u'hivtestinghistory'),
                (70L, u'bcpp_subject', u'hivtestreview'),
                (80L, u'bcpp_subject', u'hivresultdocumentation'),
                (90L, u'bcpp_subject', u'hivtested'),
                (100L, u'bcpp_subject', u'hivuntested'),
                (110L, u'bcpp_subject', u'futurehivtesting'),
                (120L, u'bcpp_subject', u'sexualbehaviour'),
                (130L, u'bcpp_subject', u'monthsrecentpartner'),
                (140L, u'bcpp_subject', u'monthssecondpartner'),
                (150L, u'bcpp_subject', u'monthsthirdpartner'),
                (160L, u'bcpp_subject', u'hivcareadherence'),
                (170L, u'bcpp_subject', u'hivmedicalcare'),
                (180L, u'bcpp_subject', u'circumcision'),
                (190L, u'bcpp_subject', u'circumcised'),
                (200L, u'bcpp_subject', u'uncircumcised'),
                (210L, u'bcpp_subject', u'reproductivehealth'),
                (220L, u'bcpp_subject', u'pregnancy'),
                (230L, u'bcpp_subject', u'nonpregnancy'),
                (240L, u'bcpp_subject', u'medicaldiagnoses'),
                (250L, u'bcpp_subject', u'heartattack'),
                (260L, u'bcpp_subject', u'cancer'),
                (270L, u'bcpp_subject', u'sti'),
                (280L, u'bcpp_subject', u'tubercolosis'),
                (290L, u'bcpp_subject', u'substanceuse'),
                (300L, u'bcpp_subject', u'stigma'),
                (310L, u'bcpp_subject', u'stigmaopinion'),
                (320L, u'bcpp_subject', u'positiveparticipant'),
                (330L, u'bcpp_subject', u'accesstocare'),
                (340L, u'bcpp_subject', u'hivresult'),
                (350L, u'bcpp_subject', u'pima'),
                (360L, u'bcpp_subject', u'subjectreferral'),
            )}
        }
    )

site_visit_schedules.register(BcppSubjectVisitSchedule)

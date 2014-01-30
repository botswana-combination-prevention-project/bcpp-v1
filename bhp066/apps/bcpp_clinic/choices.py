from django.utils.translation import ugettext as _

VISIT_REASON = [
    ('scheduled', '1. Scheduled visit/contact'),
    ('unscheduled', '2. Unscheduled visit/contact'),
    ]

VISIT_UNSCHEDULED_REASON = (
    ('walk-in', _('Walk in clinic visit')),
    ('Patient called', _('Patient called to come for visit')),
    ('OTHER', _('Other, specify:')),
)

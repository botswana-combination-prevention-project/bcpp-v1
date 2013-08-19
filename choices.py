from django.utils.translation import ugettext as _


EDUCATION = (
    ('None', _('None')),
    ('non_formal', _('Non Formal')),
    ('primary', _('Primary')),
    ('secondary', _('Secondary ')),
    ('tertiary', _('Tertiary (Higher than secondary, such as vocational college or university)')),
) 

EMPLOYMENT = (
    ('full_time', _('Full-time employed')),
    ('part_time', _('Part-time employed')),
    ('seasonal', _('Seasonal or intermittent employment')),
    ('informal', _('Informal self-employment')),
    ('student', _('Student')),
    ('retired', _('Retired')),
    ('not_woking', _('Not working (non-student, not retired)')),
    ('not_answering', _('Don\'t want to answer')),
)

MARITAL_STATUS = (
    ('single', _('Single/Never married')),
    ('cohabiting', _('Cohabitating')),
    ('married', _('Married ')),
    ('divorced', _('Divorced or formally separated')),
    ('widowed', _('Widowed')),
    ('not_answering', _('Don\'t want to answer')),
)

ALCOHOL_INTAKE = (
    ('NEVER', _('Never')),
    ('monthly', _('Monthly or less')),
    ('per_month', _('2-4 times per month')),
    ('per_week', _('2-3 times per week')),
    ('more_times', _('4 or more times per week')),
)


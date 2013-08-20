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

REASON_NOT_TESTING = (
    ('know_status', _('I already know I am HIV positive.')),
    ('not_risk',_('I don\'t believe I am at risk of getting HIV.')),
    ('afraid',_('I am afraid to find out the result.')),
    ('perception',('I am afraid of what others would think of me.')),
    ('prohibited',('Friends/Family did not want me to get an HIV test.')),
    ('time_work',('I did not have time due to work.')),
    ('time_family',('I didn\'t have time due to family obligations')),
    ('partner_refused',('My sexual partner didn\'t want me to get an HIV test')),
    ('not_sure',('I am not sure')),
    ('decline',('Decline')),
)

SYMPTOMS=(
    ('cough',('Cough > 2 weeks')),
    ('fever',('Fever > 2 weeks')),
    ('big_lymph',('Enlarged lymph nodes')),
    ('cough_blood',('Coughing up blood')),
    ('night_sweats',('Night Sweats')),
    ('weight_loss',('Unexplained weight loss')),
    ('none',('None of the above symptoms reported')),
)

REFFERED_FOR=(
    ('circumcision',('Circumcision')),
    ('cervical_screen',('Cervical Screening')),
    ('sti_screen',('STI screening')),
    ('family_plan',('Family Planning')),
    ('tb_screen',('TB screening')),
    ('couple_test',('Couple Testing')),
    ('pmtct',('PMTCT')),
    ('hiv_care',('HIV Care and Treatment')),
    ('counselling',('Supportive Counseling')),
    ('social_welfare',('Psycho social support/Social Welfare')),
)

REFFERED_TO=(
    ('health_facility',('Public/Private Health Facility')),
    ('d',('d')),
    ('religious',('Religious Institution')),
    ('plwh',('PLWH/A Association')),
    ('social_welfare',('Social Welfare facilities')),
    ('youth_friendly',('Youth Friendly Services')),
)


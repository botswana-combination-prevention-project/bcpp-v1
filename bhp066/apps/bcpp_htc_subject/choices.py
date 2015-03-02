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


PARTNER_HIV_STATUS = (
    ('positive', 'HIV Positive'),
    ('negative', 'HIV Negative'),
    ('not_sure', 'I am not sure'),
    ('declined', 'Decline to answer'),
)


RELATIONSHIP_TYPE = (
    ('spouse', 'Spouse (husband/wife)'),
    ('cohabiting', 'Cohabitating partner'),
    ('boy_girl_friend', 'Boyfriend/Girlfriend'),
    ('casual', 'Casual (known) sex partner'),
    ('partner_unknown', 'One time partner (previously unknown)'),
    ('sex_worker', 'Commercial sex worker'),
    ('OTHER', 'Other, specify'),
    ('declined', 'Decline to answer'),
)


TESTING_CENTRE = (
    ('tvct_inside_comunity', _('TVCT in this community')),
    ('tvct_outside_community', _('TVCT outside of this community')),
    ('public', _('Public Health Facility')),
    ('private', _('Private Health Facility')),
    ('door_to_door', _('Door to door projects')),
    ('other_vct_site', _('Other VCT site')),
    ('OTHER', _('Other')),
    ('dont_remember', _('Don\'t remember')),
)

YES_NO_DECLINED = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('DECLINED', _('Declined to answer')),
)


REASON_NOT_TESTING = (
    ('know_status', _('I already know I am HIV positive.')),
    ('not_risk', _('I don\'t believe I am at risk of getting HIV.')),
    ('afraid', _('I am afraid to find out the result.')),
    ('perception', _('I am afraid of what others would think of me.')),
    ('prohibited', _('Friends/Family did not want me to get an HIV test.')),
    ('time_work', _('I did not have time due to work.')),
    ('time_family', _('I didn\'t have time due to family obligations')),
    ('partner_refused', _('My sexual partner didn\'t want me to get an HIV test')),
    ('not_sure', _('I am not sure')),
    ('decline', _('Decline to answer')),
)

SYMPTOMS = (
    ('cough', _('Cough > 2 weeks')),
    ('fever', _('Fever > 2 weeks')),
    ('big_lymph', _('Enlarged lymph nodes')),
    ('cough_blood', _('Coughing up blood')),
    ('night_sweats', _('Night Sweats')),
    ('weight_loss', _('Unexplained weight loss')),
    ('none', _('None of the above symptoms reported')),
)

REFERRED_FOR = (
    ('circumcision', _('Circumcision')),
    ('cervical_screen', _('Cervical Screening')),
    ('sti_screen', _('STI screening')),
    ('family_plan', _('Family Planning')),
    ('tb_screen', _('TB screening')),
    ('couple_test', _('Couple Testing')),
    ('pmtct', _('PMTCT')),
    ('hiv_care', _('HIV Care and Treatment')),
    ('counselling', _('Supportive Counseling')),
    ('social_welfare', _('Psycho social support/Social Welfare')),
)

REFERRED_TO = (
    ('health_facility', _('Public/Private Health Facility')),
    ('religious', _('Religious Institution')),
    ('plwh', _('PLWH/A Association')),
    ('social_welfare', _('Social Welfare facilities')),
    ('youth_friendly', _('Youth Friendly Services')),
)

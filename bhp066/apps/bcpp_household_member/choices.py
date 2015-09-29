from django.utils.translation import ugettext as _

from .constants import (ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE,
                        NOT_REPORTED, REFUSED, UNDECIDED, REFUSED_HTC, BHS_LOSS, ANNUAL, DECEASED,
                        HEAD_OF_HOUSEHOLD)

options = list(set([ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE,
                    NOT_REPORTED, REFUSED, UNDECIDED, REFUSED_HTC, BHS_LOSS, ANNUAL, DECEASED]))

HOUSEHOLD_MEMBER_PARTICIPATION = [(item, item) for item in options]

FEMALE_RELATIONS = [
    ('wife', 'Wife'),
    ('daughter', 'Daughter'),
    ('mother', 'Mother'),
    ('sister', 'Sister'),
    ('grandmother', 'Grandmother'),
    ('granddaughter', 'Granddaughter'),
    ('great-Grandmother', 'Great-Grandmother'),
    ('great-Granddaughter', 'Great-Granddaughter'),
    ('aunt', 'Aunt'),
    ('niece', 'Niece'),
    ('mother-in-law', 'Mother-in-law'),
    ('daughter-in-law', 'Daughter-in-law'),
    ('sister-in-law', 'Sister-in-law'),
    ('housemaid', 'Housemaid'),
]

ANY_RELATIONS = [
    ('partner', 'Partner'),
    ('housemate', 'Housemate'),
    ('cousin', 'Cousin'),
    ('family_friend', 'Family friend'),
    ('friend', 'Friend'),
    ('helper', 'Helper'),
    ('employee', 'Employee'),
]
MALE_RELATIONS = [
    ('husband', 'Husband'),
    ('son', 'Son'),
    ('father', 'Father'),
    ('brother', 'Brother'),
    ('grandfather', 'Grandfather'),
    ('grandson', 'Grandson'),
    ('great-Grandfather', 'Great-Grandfather'),
    ('great-Grandson', 'Great-Grandson'),
    ('uncle', 'Uncle'),
    ('nephew', 'Nephew'),
    ('father-in-law', 'Father-in-law'),
    ('son-in-law', 'Son-in-law'),
    ('brother-in-law', 'Brother in-law'),
]


relations = FEMALE_RELATIONS + MALE_RELATIONS + ANY_RELATIONS
relations.sort()
RELATIONS = [(HEAD_OF_HOUSEHOLD, 'HEAD of HOUSEHOLD')] + relations + [('UNKNOWN', 'UNKNOWN')]

ABSENTEE_STATUS = (
    ('ABSENT', _('Absent')),
    ('NOT_ABSENT', _('No longer absent')),
)

ABSENTEE_REASON = (
    ('gone visiting (relatives,holidays,weddings,funerals)', _('Gone visiting')),
    ('stays at lands or cattlepost ', _('Stays at Lands/Cattlepost ')),
    ('stepped out(shops, errands etc) ', _('Stepped out (shops, errands, ) ')),
    ('works in village and comes home daily', _('Works in the village, home daily')),
    ('goes to school in village and comes home daily', _('Schools in this village, home daily')),
    ('works outside village and comes home daily', _('Works outside the village, home daily')),
    ('goes to school outside village and comes home daily', _('Schools outside village, home daily')),
    ('works outside village and comes home irregularly ', _('Works outside the village, home irregularly ')),
    ('goes to school outside village and comes home irregularly ', _('Schools outside village, home irregularly ')),
    ('works outside village and comes home monthly ', _('Works outside the village, home monthly ')),
    ('goes to school outside village and comes home monthly ', _('Schools outside village, home monthly ')),
    ('works outside village and comes home on weekends ', _('Works outside the village, home on weekends ')),
    ('goes to school outside village and comes home on weekends ', _('Schools outside village, home on weekends ')),
    ('OTHER', _('Other...')),
)

NEXT_APPOINTMENT_SOURCE = (
    ('participant', _('Participant')),
    ('household member', _('household member')),
    ('hbc', _('HBC')),
    ('other', _('Other'))
)

MOVED_REASON = (
    ('TRANSFER', _('Job Transfer')),
    ('MARRIAGE', _('Marriage')),
    ('INDEPENDENT', _('Independence')),
    ('OTHER', _('Other')),
)

PLACE_SUBJECT_MOVED = (
    ('IN_VILLAGE', _('Within Village')),
    ('OUT_VILLAGE', _('Outside Village')),
)

UNDECIDED_REASON = (
    ('afraid_to_test', _('afraid_to_test')),
    ('not ready to test', _('not ready to test')),
    ('wishes to test with partner', _('wishes to test with partner')),
    ('OTHER', _('Other...')),
)

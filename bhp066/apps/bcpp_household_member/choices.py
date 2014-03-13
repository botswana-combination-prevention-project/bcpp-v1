from django.utils.translation import ugettext as _

HOUSEHOLD_MEMBER_FULL_PARTICIPATION = [
    ('NOT_REPORTED', '<not reported>'),
    ('RESEARCH', 'BHS'),
#     ('HTC', 'HTC'),
#     ('RBD', 'RBD only'),
    ('ABSENT', 'Absentee'),
    ('REFUSED', 'Refusal'),
    ('UNDECIDED', 'Undecided'),
    #('NOT_ELIGIBLE', 'Not Eligible'),
]

HOUSEHOLD_MEMBER_NOT_ELIGIBLE = [
    ('NOT_ELIGIBLE', 'Not Eligible'),
]

HOUSEHOLD_MEMBER_HTC = [
    ('NOT_REPORTED', '<not reported>'),
    ('HTC', 'HTC'),
]

HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION = [
    ('NOT_REPORTED', '<not reported>'),
    ('RBD', 'RBD only'),
    ('HTC', 'HTC'),
    ('HTC/RBD', 'HTC plus RBD'),
]

HOUSEHOLD_MEMBER_MINOR = [
    ('NOT_REPORTED', '<not reported>'),
    ('NOT_ELIGIBLE', 'Not Eligible'),
]

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
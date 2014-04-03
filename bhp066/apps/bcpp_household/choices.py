from .constants import (ELIGIBLE_REPRESENTATIVE_PRESENT, ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                        REFUSED_ENUMERATION, RESIDENTIAL_HABITABLE, NEARLY_ALWAYS_OCCUPIED, SEASONALLY_OCCUPIED, RARELY_OCCUPIED, NEVER_OCCUPIED, UNKNOWN,
                        NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, TWENTY_PERCENT, FIVE_PERCENT)

HOUSEHOLD_STATUS = (
    (ELIGIBLE_REPRESENTATIVE_PRESENT, 'Eligible Representative Present'),
    (ELIGIBLE_REPRESENTATIVE_ABSENT, 'Eligible Representative Absent'),
    (NO_HOUSEHOLD_INFORMANT, 'No Household Informant'),
    (REFUSED_ENUMERATION, 'Refused Enumeration'),
    )


BCPP_VILLAGES = (
    (1, 'Dikwididi'),
    (2, 'Gabane'),
    (3, 'Hatsalatladi'),
    (4, 'Kumakwane'),
    (5, 'Lentsweletau'),
    (6, 'Lerala'),
    (7, 'Machaneng'),
    (8, 'Makalamabedi'),
    (9, 'Mapoka'),
    (10, 'Matsiloje'),
    (11, 'Mookane'),
    (12, 'Otse'),
    (13, 'Radisele'),
    (14, 'Rakops'),
    (15, 'Sefophe'),
    (16, 'Serowe'),
    (99, 'Other'),
    (999, 'Not specified'),
)

BCPP_WARDS = (
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
)


INFO_PROVIDER = (
    ('SUBJECT', 'Subject'),
    ('NEXT_OF_KIN', 'Kin'),
    ('OTHER', 'Other'))

PLOT_STATUS = (
    (NON_RESIDENTIAL, 'non-residential'),
    (RESIDENTIAL_NOT_HABITABLE, 'residential, not-habitable'),
    (RESIDENTIAL_HABITABLE, 'residential, habitable'),
    )

PLOT_LOG_STATUS = (
    ('ACCESSIBLE', 'Accessible'),
    ('INACCESSIBLE', 'Inaccessible'),
)

NOT_ENUMERATED_REASONS = (
        ('hoh_refused', 'HOH refusal'),
        ('no_household_informant', 'No Household Informant'),
)

HOUSEHOLD_COMPLETION_STATUS = (
    ('complete', 'Complete'),
    ('incomplete', 'Incomplete'),
    )


STATUS = (
    ('within_bcpp_area', 'In BCPP Village'),
    ('moved', 'No longer lives here'),
    ('deceased', 'Deceased'),
    ("OTHER", 'Other'),
)

SELECTED = (
    (TWENTY_PERCENT, 'twenty_percent'),
    (FIVE_PERCENT, 'five_percent'),
)

SECTIONS = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

SUB_SECTIONS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
)

INELIGIBLE_REASON = (
    ('non_citizen', 'Non-Citizen(s)'),
    ('age_ineligible', 'Not of eligible age'),
    ('other', 'Other'),
    )

RESIDENT_LAST_SEEN = (
    (NEARLY_ALWAYS_OCCUPIED, 'at least 1 person stays in the household for at least half the nights in the year'),  # replace
    (SEASONALLY_OCCUPIED, 'at least 1 person stays in the household for at least 4 weeks but less than half the nights over the past year'),  # replace
    (RARELY_OCCUPIED, 'at least 1 person stays in the household for 1 or more nights but less than 4 weeks over the past year'),  # NOT replaced
    (NEVER_OCCUPIED, 'nobody spent at least 1 night in the household over the past year'),  # NOT replaced
    (UNKNOWN, 'Don\'t know'),  # replaced
)

NEXT_APPOINTMENT_SOURCE = (('neighbour', 'Neighbour'), ('household member', 'Household Member'), ('hbc', 'Field RA'), ('other', 'Other'))

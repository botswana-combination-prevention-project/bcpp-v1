from edc.constants import COMPLETE, INCOMPLETE

from .constants import (ELIGIBLE_REPRESENTATIVE_PRESENT, ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                        REFUSED_ENUMERATION, RESIDENTIAL_HABITABLE, RARELY_NEVER_OCCUPIED,
                        SEASONALLY_NEARLY_ALWAYS_OCCUPIED, UNKNOWN_OCCUPIED,
                        NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, TWENTY_PERCENT, FIVE_PERCENT,
                        INACCESSIBLE, ACCESSIBLE)

HOUSEHOLD_LOG_STATUS = (
    (ELIGIBLE_REPRESENTATIVE_PRESENT, 'Eligible Representative Present'),
    (ELIGIBLE_REPRESENTATIVE_ABSENT, 'Eligible Representative Absent'),
    (NO_HOUSEHOLD_INFORMANT, 'No Household Informant'),
    (REFUSED_ENUMERATION, 'Refused Enumeration'),
)

# as used by HSPH
HH_STATUS = (
    ('ineligible', 'ineligible'),
    ('not_enum_hh', 'not_enum_hh'),
    ('not_enum_never_there', 'not_enum_never_there'),
    ('not_enum_rarely_there', 'not_enum_rarely_there'),
    ('not_enum_seasonally_occupied', 'not_enum_seasonally_occupied'),
    ('not_enum_almost_always_there', 'not_enum_almost_always_there'),
    ('not_enum_unknown_status', 'not_enum_unknown_status'),
    ('not_enum_hh_refused', 'not_enum_hh_refused'),
    ('enumerated_not_enrolled', 'enumerated_not_enrolled'),
    ('enrolled', 'enrolled'),
)

HOUSEHOLD_REFUSAL = (
    ('not_interested', 'Not Interested'),
    ('does_not_have_time', 'Does not have time'),
    ('DWTA', 'Don\'t want to answer'),
    ('OTHER', 'Other'),
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
    (INACCESSIBLE, 'Inaccessible'),
)

PLOT_LOG_STATUS = (
    (ACCESSIBLE, 'Accessible'),
    (INACCESSIBLE, 'Inaccessible'),
)

NOT_ENUMERATED_REASONS = (
    ('hoh_refused', 'HOH refusal'),
    ('no_household_informant', 'No Household Informant'),
)

HOUSEHOLD_COMPLETION_STATUS = (
    (COMPLETE, 'Complete'),
    (INCOMPLETE, 'Incomplete'),
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
    (SEASONALLY_NEARLY_ALWAYS_OCCUPIED, (
        'spent at least 4 weeks in household over the course of the past year')
     ),  # replace
    (RARELY_NEVER_OCCUPIED, 'pent less than 4 weeks in the household  over the course of the'
     'past year, or never occupied over the course of the past year'),  # NOT replaced
    (UNKNOWN_OCCUPIED, 'Don\'t know'),  # replaced
)

INACCESSIBILITY_REASONS = (
    ('impassable_road', 'Road is impassable'),
    ('dogs', 'Dogs prevent access'),
    ('locked_gate', 'Gate is locked'),
    ('OTHER', 'Other'),
)

NEXT_APPOINTMENT_SOURCE = (
    ('neighbour', 'Neighbour'),
    ('household member', 'Household Member'),
    ('hbc', 'Field RA'), ('other', 'Other')
)

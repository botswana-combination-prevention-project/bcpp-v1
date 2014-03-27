from .constants import ELIGIBLE_REPRESENTATIVE_PRESENT, ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION

options = list(set([ELIGIBLE_REPRESENTATIVE_PRESENT, ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT, REFUSED_ENUMERATION]))
options.sort()
HOUSEHOLD_STATUS = [(item, item) for item in options]


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
    ('non-residential', 'non-residential'),
    ('residential_not_habitable', 'residential, not-habitable'),
    ('residential_habitable', 'residential, habitable'),
    )

PLOT_LOG_STATUS = (
    ('ACCESSIBLE', 'Accessible'),
    ('INACCESSIBLE', 'Inaccessible'),
)

NOT_ENUMERATED_REASONS = (
        ('HOH_refued', 'HOH refusal'),
        ('no_household_informant', 'No Household Informant'),
)

HOUSEHOLD_COMPLETION_STATUS = (
    ('complete', 'Complete'),
    ('incomplete', 'Incomplete'),
    )


STATUS = (
    ('WITHIN_BCPP_AREA', 'In BCPP Village'),
    ('MOVED', 'No longer lives here'),
    ('DECEASED', 'Deceased'),
    ("OTHER", 'Other'),
)

SELECTED = (
            (1, 'twenty_percent'),
            (2, 'five_percent'),
)

ENUMERATION_STATUS = (
    ('yes', 'Yes'),
    ('no', 'No')
)

YES_NO = (
    ('yes', 'Yes'),
    ('no', 'No')
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
        ('4_weeks_a_year', 'Spends at least 4 weeks in a household over the course of the past year '),
        ('1_night_less_than_4_weeks_year', 'spends at least 1 night be probably less than 4 weeks/year in the household'),
        ('never_spent_1_day_over_a_year', 'did not even spend 1 night in the household over the past year'),
        ('dont_know', 'Don\'t know'),
)

NEXT_APPOINTMENT_SOURCE = (('neighbour', 'Neighbour'), ('household member', 'Household Member'), ('hbc', 'Field RA'), ('other', 'Other'))

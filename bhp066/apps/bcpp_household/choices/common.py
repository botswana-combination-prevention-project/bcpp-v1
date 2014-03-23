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

HOUSEHOLD_STATUS = (
    ('eligible_representative_present', 'HOH or eligible representative present'),
    ('eligible_representative_absent', 'HOH or eligible representative absent, ineligible household member present'),
    ('no_household_informant', 'No household informant'),
    ('refused', 'refused'),
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


RESIDENT_LAST_SEEN = (
        ('more_than_a_year', 'More than one year ago '),
        ('1_to_6_months', '1-6 months ago'),
        ('7_to_12_months', '7- 12 months'),
        ('less_than_a_month_ago', 'Less than a month ago'),
)

NEXT_APPOINTMENT_SOURCE = (('neighbour', 'Neighbour'), ('household member', 'Household Member'), ('hbc', 'Field RA'), ('other', 'Other'))

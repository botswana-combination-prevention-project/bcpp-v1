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

STATUS = (
    ('WITHIN_BCPP_AREA', 'In BCPP Village'),
    ('MOVED', 'No longer lives here'),
    ('DECEASED', 'Deceased'),
    ("OTHER", 'Other'),
)


RELATIONS = (
    ('SELF', 'SELF'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Daughter', 'Daughter'),
    ('Partner', 'Partner'),
    ('housemate', 'Housemate'),
    ('Son', 'Son'),
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sister', 'Sister'),
    ('Brother', 'Brother'),
    ('Grandmother', 'Grandmother'),
    ('Grandfather', 'Grandfather'),
    ('Granddaughter', 'Granddaughter'),
    ('Grandson', 'Grandson'),
    ('Great-Grandmother', 'Great-Grandmother'),
    ('Great-Grandfather', 'Great-Grandfather'),
    ('Great-Granddaughter', 'Great-Granddaughter'),
    ('Great-Grandson', 'Great-Grandson'),
    ('Aunt', 'Aunt'),
    ('Uncle', 'Uncle'),
    ('Nephew', 'Nephew'),
    ('Niece', 'Niece'),
    ('COUSIN', 'Cousin'),
    ('mother-in-law', 'Mother-in-law'),
    ('father-in-law', 'Father-in-law'),
    ('Daughter-in-law', 'Daughter-in-law'),
    ('Son-in-law', 'Son-in-law'),
    ('sister-in-law', 'Sister-in-law'),
    ('brother in-law', 'Brother in-law'),
    ('FAMILY FRIEND', 'Family friend'),
    ('friend', 'Friend'),
    ('helper', 'Helper'),
    ('HOUSEMAID', 'Housemaid'),
    ('EMPLOYEE', 'Employee'),
    ('UNKNOWN', 'UNKNOWN'),
    )


HOUSEHOLD_MEMBER_ACTION = [
    ('NOT_REPORTED', '<not reported>'),
    ('CONSENTING', 'Consenting'),
    ('ABSENT', 'Absentee'),
    ('REFUSED', 'Refusal'),
    ('OTHER', 'Other'),
]

NEXT_APPOINTMENT_SOURCE = (('neighbour', 'Neighbour'), ('household member', 'Household Member'), ('hbc', 'HBC'), ('other', 'Other'))

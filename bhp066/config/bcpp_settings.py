from datetime import date

"""This file should have attributes that are specific to BCPP.

Dates: Dates specific to a BHS campaign.
       These dates need to be set for each campaign.
       See also bcpp_household.mappers
"""

APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROTOCOL_REVISION = 'V1.0 24 September 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'

BHS_START_DATE = date(2014, 9, 4)
BHS_FULL_ENROLLMENT_DATE = date(2014, 10, 15)
BHS_END_DATE = date(2014, 10, 31)
SMC_START_DATE = date(2014, 10, 27)  # referenced by bcpp mappers
SMC_ECC_START_DATE = date(2014, 10, 29)  # referenced by bcpp mappers

MAX_HOUSEHOLDS_PER_PLOT = 9  # see plot models

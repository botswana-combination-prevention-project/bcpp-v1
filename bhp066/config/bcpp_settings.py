"""This file has attributes that are specific to BCPP.

See also bcpp_household.mappers
"""
from datetime import datetime

APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROTOCOL_REVISION = 'V1.0 24 September 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'
CURRENT_SURVEY = 'bcpp-year-2'
MAX_HOUSEHOLDS_PER_PLOT = 9  # see plot models
LIMIT_EDIT_TO_CURRENT_SURVEY = True
LIMIT_EDIT_TO_CURRENT_COMMUNITY = True
FILTERED_DEFAULT_SEARCH = True
STUDY_OPEN_DATETIME = datetime(2013, 10, 18, 0, 0, 0)

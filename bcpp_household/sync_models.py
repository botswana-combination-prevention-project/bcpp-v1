from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'bcpp_household.householdassessment',
    'bcpp_household.gpsdevice',
    'bcpp_household.household',
    'bcpp_household.householdidentifierhistory',
    'bcpp_household.householdlog',
    'bcpp_household.householdlogentry',
    'bcpp_household.householdrefusal',
    'bcpp_household.householdrefusalhistory',
    'bcpp_household.householdstructure',
    'bcpp_household.householdworklist',
    'bcpp_household.increaseplotradius',
    'bcpp_household.plot',
    'bcpp_household.plotidentifierhistory',
    'bcpp_household.plotlog',
    'bcpp_household.plotlogentry',
    'bcpp_household.representativeeligibility']

site_sync_models.register(sync_models, SyncModel)

from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = [
    'bcpp_household_member.enrollmentchecklist',
    'bcpp_household_member.subjectabsentee',
    'bcpp_household_member.subjectabsenteeentry',
    'bcpp_household_member.subjectdeath',
    'bcpp_household_member.subjecthtc',
    'bcpp_household_member.subjecthtchistory',
    'bcpp_household_member.subjectmoved',
    'bcpp_household_member.subjectrefusal',
    'bcpp_household_member.subjectrefusalhistory',
    'bcpp_household_member.subjectundecided',
    'bcpp_household_member.subjectundecidedentry',
    'bcpp_household_member.enrollmentloss',
    'bcpp_household_member.householdheadeligibility',
    'bcpp_household_member.householdinfo',
    'bcpp_household_member.householdmember',
    'bcpp_household_member.memberappointment']

site_sync_models.register(sync_models, SyncModel)

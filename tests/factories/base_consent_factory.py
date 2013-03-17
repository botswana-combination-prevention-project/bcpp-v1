import factory
from datetime import datetime
from bhp_variables.tests.factories import StudySiteFactory
from bhp_base_model.tests.factories import BaseUuidModelFactory


class BaseConsentFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    study_site = factory.SubFactory(StudySiteFactory)
    consent_datetime = datetime.today()
    may_store_samples = 'Yes'
    is_incarcerated = 'No'

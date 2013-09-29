import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import AccessToCare


class AccessToCareFactory(BaseUuidModelFactory):
    FACTORY_FOR = AccessToCare

    report_datetime = datetime.today()

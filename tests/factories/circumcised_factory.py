import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Circumcised


class CircumcisedFactory(BaseUuidModelFactory):
    FACTORY_FOR = Circumcised

    report_datetime = datetime.today()

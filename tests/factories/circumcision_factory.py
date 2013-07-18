import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Circumcision


class CircumcisionFactory(BaseUuidModelFactory):
    FACTORY_FOR = Circumcision

    report_datetime = datetime.today()
    circumcised = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]

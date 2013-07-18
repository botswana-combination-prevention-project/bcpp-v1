import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivUntested


class HivUntestedFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivUntested

    report_datetime = datetime.today()
    hiv_pills = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]

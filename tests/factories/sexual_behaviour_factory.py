import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourFactory(BaseUuidModelFactory):
    FACTORY_FOR = SexualBehaviour

    report_datetime = datetime.today()
    ever_sex = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]

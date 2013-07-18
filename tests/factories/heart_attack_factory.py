import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HeartAttack


class HeartAttackFactory(BaseUuidModelFactory):
    FACTORY_FOR = HeartAttack

    report_datetime = datetime.today()
    date_heart_attack = date.today()

import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HeartAttack


class HeartAttackFactory(BaseUuidModelFactory):
    FACTORY_FOR = HeartAttack

    report_datetime = datetime.today()
    date_heart_attack = date.today()
    dx_heart_attack_other = factory.Sequence(lambda n: 'dx_heart_attack_other{0}'.format(n))

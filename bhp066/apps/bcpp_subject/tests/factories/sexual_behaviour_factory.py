import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import SexualBehaviour


class SexualBehaviourFactory(BaseUuidModelFactory):
    FACTORY_FOR = SexualBehaviour

    report_datetime = datetime.today()
    ever_sex = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]

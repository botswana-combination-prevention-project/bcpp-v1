import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Circumcision


class CircumcisionFactory(BaseUuidModelFactory):
    FACTORY_FOR = Circumcision

    report_datetime = datetime.today()
    circumcised = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]

import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Uncircumcised


class UncircumcisedFactory(BaseUuidModelFactory):
    FACTORY_FOR = Uncircumcised

    report_datetime = datetime.today()
    future_circ = (('Yes', u'Yes'), ('No', u'No'), ('not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]

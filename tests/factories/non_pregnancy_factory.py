import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import NonPregnancy


class NonPregnancyFactory(BaseUuidModelFactory):
    FACTORY_FOR = NonPregnancy

    report_datetime = datetime.today()
    last_birth = date.today()
    anc_last_pregnancy = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    more_children = (('Yes', u'Yes'), ('No', u'No'), ('not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]

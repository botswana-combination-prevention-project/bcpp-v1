import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubstanceUse


class SubstanceUseFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubstanceUse

    report_datetime = datetime.today()
    alcohol = (('Never', u'Never'), ('Less then once a week', u'Less then once a week'), ('Once a week', u'Once a week'), ('2 to 3 times a week', u'2 to 3 times a week'), ('more than 3 times a week', u'more than 3 times a week'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    smoke = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]

import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_htc_subject.models import PositiveFollowup
from htc_subject_visit_factory import HtcSubjectVisitFactory


class PositiveFollowupFactory(BaseUuidModelFactory):
    FACTORY_FOR = PositiveFollowup

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    contact_consent = (('Yes', u'Yes'), ('No', u'No'))[0][0]
    contact_family = (('Yes', u'Yes'), ('No', u'No'))[0][0]

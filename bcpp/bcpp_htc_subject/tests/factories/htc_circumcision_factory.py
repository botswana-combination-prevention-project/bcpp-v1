import factory

from datetime import date, datetime

from ...models import HtcCircumcision

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class HtcCircumcisionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HtcCircumcision

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    is_circumcised = (('Yes', u'Yes'), ('No', u'No'))[0][0]

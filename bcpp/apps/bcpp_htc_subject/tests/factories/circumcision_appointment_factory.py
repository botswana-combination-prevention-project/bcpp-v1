import factory

from datetime import datetime

from ...models import CircumcisionAppointment

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class CircumcisionAppointmentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CircumcisionAppointment

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    circumcision_ap = (('Yes', u'Yes'), ('No', u'No'))[0][0]

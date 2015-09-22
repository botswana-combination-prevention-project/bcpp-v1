import factory
from datetime import date, datetime

from ...models import Cd4Test

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class Cd4TestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Cd4Test

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    cd4_test_date = date.today()
    cd4_result = 2.5
    referral_clinic = factory.Sequence(lambda n: 'referral_clinic{0}'.format(n))
    appointment_date = date.today()

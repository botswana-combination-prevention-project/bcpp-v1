from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import SubjectReferral


class SubjectReferralFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectReferral

    report_datetime = datetime.today()

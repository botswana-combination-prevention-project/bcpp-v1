import factory
from datetime import date, datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HtcSubjectLocator


class HtcSubjectLocatorFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcSubjectLocator

    report_datetime = datetime.today()
    date_signed = date.today()
    home_visit_permission = 'Yes'
    may_follow_up = 'Yes'
    may_call_work = 'Yes'
    may_contact_someone = 'Yes'
    has_alt_contact = 'Yes'

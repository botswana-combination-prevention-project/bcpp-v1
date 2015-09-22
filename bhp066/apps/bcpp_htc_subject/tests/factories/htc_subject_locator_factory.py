import factory
from datetime import date, datetime

from ...models import HtcSubjectLocator


class HtcSubjectLocatorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HtcSubjectLocator

    report_datetime = datetime.today()
    date_signed = date.today()
    home_visit_permission = 'Yes'
    may_follow_up = 'Yes'
    may_call_work = 'Yes'
    may_contact_someone = 'Yes'
    has_alt_contact = 'Yes'

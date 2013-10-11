import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HivTestReview


class HivTestReviewFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestReview

    report_datetime = datetime.today()
    hiv_test_date = date.today()
    recorded_hiv_result = (('POS', u'HIV Positive (Reactive)'), ('NEG', u'HIV Negative (Non-reactive)'), ('IND', u'Indeterminate'), ('No result recorded', u'No result recorded'))[0][0]

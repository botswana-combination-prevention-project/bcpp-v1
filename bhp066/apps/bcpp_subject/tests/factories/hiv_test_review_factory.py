import factory

from datetime import date, datetime

from ...models import HivTestReview


class HivTestReviewFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTestReview

    report_datetime = datetime.today()
    hiv_test_date = date.today()
    recorded_hiv_result = (('POS', u'HIV Positive (Reactive)'), ('NEG', u'HIV Negative (Non-reactive)'), ('IND', u'Indeterminate'), ('No result recorded', u'No result recorded'))[0][0]

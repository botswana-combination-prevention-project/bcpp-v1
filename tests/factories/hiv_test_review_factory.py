import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivTestReview


class HivTestReviewFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestReview

    report_datetime = datetime.today()
    hiv_test_date = date.today()
    recorded_hiv_result = (('POS', 'HIV Positive (Reactive)'), ('NEG', 'HIV Negative (Non-reactive)'), ('IND', 'Indeterminate'), ('No result recorded', 'No result recorded'))[0][0]

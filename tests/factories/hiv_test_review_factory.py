import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivTestReview


class HivTestReviewFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivTestReview

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    hiv_test_date = date.today()
    recorded_hiv_result = (('HIV-Negative', 'HIV Negative (Non-reactive)'), ('HIV-Positive', 'HIV Positive (Reactive)'), ('Indeterminate', 'Indeterminate'), ('No result recorded', 'No result recorded'))[0][0]

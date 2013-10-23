import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import SubjectReferral
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory


class SubjectReferralFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectReferral

    report_datetime = datetime.today()
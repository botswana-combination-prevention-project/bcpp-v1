import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import PositiveParticipant


class PositiveParticipantFactory(BaseScheduledModelFactory):
    FACTORY_FOR = PositiveParticipant

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    internalize_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    internalized_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    friend_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    family_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_talk_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_respect_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_jobs_tigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]

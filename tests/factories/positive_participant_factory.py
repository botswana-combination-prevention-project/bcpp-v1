import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import PositiveParticipant


class PositiveParticipantFactory(BaseUuidModelFactory):
    FACTORY_FOR = PositiveParticipant

    report_datetime = datetime.today()
    internalize_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    internalized_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    friend_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    family_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_talk_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_respect_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_jobs_tigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]

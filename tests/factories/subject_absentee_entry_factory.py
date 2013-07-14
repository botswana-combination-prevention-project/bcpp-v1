import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectAbsenteeEntry
from bcpp_subject.tests.factories import SubjectAbsenteeFactory


class SubjectAbsenteeEntryFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectAbsenteeEntry

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    next_appt_datetime = datetime.today()
    next_appt_datetime_source = (('participant', 'Participant'), ('household member', 'household member'), ('hbc', 'HBC'), ('other', 'Other'))[0][0]
    subject_absentee = factory.SubFactory(SubjectAbsenteeFactory)
    reason = (('gone visiting (relatives,holidays,weddings,funerals)', 'Gone visiting'), ('stays at lands or cattlepost ', 'Stays at Lands/Cattlepost '), ('stepped out(shops, errands etc) ', 'Stepped out (shops, errands, ) '), ('works in village and comes home daily', 'Works in the village, home daily'), ('goes to school in village and comes home daily', 'Schools in this village, home daily'), ('works outside village and comes home daily', 'Works outside the village, home daily'), ('goes to school outside village and comes home daily', 'Schools outside village, home daily'), ('works outside village and comes home irregularly ', 'Works outside the village, home irregularly '), ('goes to school outside village and comes home irregularly ', 'Schools outside village, home irregularly '), ('works outside village and comes home monthly ', 'Works outside the village, home monthly '), ('goes to school outside village and comes home monthly ', 'Schools outside village, home monthly '), ('works outside village and comes home on weekends ', 'Works outside the village, home on weekends '), ('goes to school outside village and comes home on weekends ', 'Schools outside village, home on weekends '), ('OTHER', 'Other...'))[0][0]

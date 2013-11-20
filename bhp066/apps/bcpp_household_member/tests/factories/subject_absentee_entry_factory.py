import factory
from datetime import date, datetime, timedelta
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import SubjectAbsenteeEntry
from ..factories import SubjectAbsenteeFactory


class SubjectAbsenteeEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectAbsenteeEntry

    subject_absentee = factory.SubFactory(SubjectAbsenteeFactory)  
    report_datetime = factory.Sequence(lambda n: datetime.now() + timedelta(days=int(n)))
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    next_appt_datetime = datetime.today()
    next_appt_datetime_source = (('participant', u'Participant'), ('household member', u'household member'), ('hbc', u'HBC'), ('other', u'Other'))[0][0]
    #subject_absentee = factory.SubFactory(SubjectAbsenteeFactory)
    reason = (('gone visiting (relatives,holidays,weddings,funerals)', u'Gone visiting'), ('stays at lands or cattlepost ', u'Stays at Lands/Cattlepost '), ('stepped out(shops, errands etc) ', u'Stepped out (shops, errands, ) '), ('works in village and comes home daily', u'Works in the village, home daily'), ('goes to school in village and comes home daily', u'Schools in this village, home daily'), ('works outside village and comes home daily', u'Works outside the village, home daily'), ('goes to school outside village and comes home daily', u'Schools outside village, home daily'), ('works outside village and comes home irregularly ', u'Works outside the village, home irregularly '), ('goes to school outside village and comes home irregularly ', u'Schools outside village, home irregularly '), ('works outside village and comes home monthly ', u'Works outside the village, home monthly '), ('goes to school outside village and comes home monthly ', u'Schools outside village, home monthly '), ('works outside village and comes home on weekends ', u'Works outside the village, home on weekends '), ('goes to school outside village and comes home on weekends ', u'Schools outside village, home on weekends '), ('OTHER', u'Other...'))[0][0]

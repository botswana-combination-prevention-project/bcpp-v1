import factory

from datetime import datetime, timedelta

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import SubjectUndecidedEntry

from ..factories import SubjectUndecidedFactory


class SubjectUndecidedEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectUndecidedEntry

    report_datetime = factory.Sequence(lambda n: datetime.now() + timedelta(days=int(n)))
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    next_appt_datetime = datetime.today()
    next_appt_datetime_source = (('participant', u'Participant'), ('household member', u'household member'), ('hbc', u'HBC'), ('other', u'Other'))[0][0]
    subject_undecided = factory.SubFactory(SubjectUndecidedFactory)
    subject_undecided_reason = (('afraid_to_test', u'afraid_to_test'), ('not ready to test', u'not ready to test'), ('wishes to test with partner', u'wishes to test with partner'), ('OTHER', u'Other...'))[0][0]

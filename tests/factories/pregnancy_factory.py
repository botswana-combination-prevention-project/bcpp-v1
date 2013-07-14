import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Pregnancy


class PregnancyFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Pregnancy

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    more_children = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    where_circ = (('Yes', 'Yes'), ('No, not sexually active and will not become sexual active', 'No, not sexually active and will not become sexual active'), ('No, prior surgical sterilization', 'No, prior surgical sterilization'), ('No, partner(s) surgically sterilized', 'No, partner(s) surgically sterilized'), ('No, post-menopause', 'No, post-menopause (at least 24 consecutive months without a period)'), ('Other, specify:', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    family_planning_other = factory.Sequence(lambda n: 'family_planning_other{0}'.format(n))
    current_pregnant = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    lnmp = date.today()
    last_birth = date.today()
    anc_last_pregnancy = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hiv_last_pregnancy = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
    preg_arv = (('Yes, AZT (single drug, twice a day)', 'Yes, AZT (single drug, twice a day)'), ('Yes, HAART ', 'Yes, HAART [multiple drugs like Atripla, Truvada, or Combivir taken once or twice a day]'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"), ('No', "No ARV's"))[0][0]

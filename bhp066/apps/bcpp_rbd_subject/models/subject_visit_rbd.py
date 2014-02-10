from apps.bcpp_subject.models import SubjectVisit


class SubjectVisitRBD(SubjectVisit):

    class Meta:
        verbose_name = 'Research Blood Draw Subject Visit'
        app_label = 'bcpp_rbd_subject'

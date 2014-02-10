from apps.bcpp_subject.models import SubjectLocator


class SubjectLocatorRBD(SubjectLocator):

    class Meta:
        verbose_name = 'Research Blood Draw Subject Locator'
        app_label = 'bcpp_rbd_subject'

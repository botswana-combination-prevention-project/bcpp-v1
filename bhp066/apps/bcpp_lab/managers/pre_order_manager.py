from django.db import models


class PreOrderManager(models.Manager):

    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk, name):
        SubjectVisit = models.get_model('bcpp_subject', 'SubjectVisit')
        Panel = models.get_model('bcpp_lab', 'Panel')
        panel = Panel.objects.get(name=name)
        subject_visit = SubjectVisit.objects.get_by_natural_key(report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(subject_visit=subject_visit, panel=panel)
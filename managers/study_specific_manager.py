from django.db import models
from django.db.models.query import QuerySet


class StudySpecificManager(models.Manager):

    def get_query_set(self):
        qs = QuerySet(self.model, using=self._db).all()
        if not qs:
            return qs
            raise ValueError('Application is accessing model StudySpecific but you have not populated it. Please do so before continuing.')
        qs = QuerySet(self.model, using=self._db).filter(pk=qs[0].pk)
        return qs

    def get_subject_types(self):
        if super(StudySpecificManager, self).all():
            if not super(StudySpecificManager, self).all()[0].subject_type:
                raise TypeError('Please indicate the subject types for this protocol in model StudySpecific. e.g. \'subject\' or \'maternal, infant\', etc')
        else:
            raise ValueError('Application is accessing model StudySpecific but you have not populated it. Please do so before continuing.')
        return super(StudySpecificManager, self).all()[0].subject_type.split(', ')
